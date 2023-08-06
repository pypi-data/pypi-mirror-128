from omnitools import FTPSC, parse_credentials_argv, getpw, dt2yyyymmddhhmmss, md5, b64e, b64d
from aescipher import AESCipherCTRFileEncReader, AESCipherCTRFileDecWriter
from html import escape, unescape
from .helper import UC
from .utils import csm
import traceback
import threading
import sqlq
import time
import re
import os


class UC_FTP(UC):
    ftp_domain = "ftp.userscloud.com"
    ftp_port = 975
    cwd = None
    terminate = False
    terminated = True
    sqlqueue = None

    def __init__(self, *args, debug: bool = False, **kwargs):
        super().__init__(debug=debug)
        self.c = FTPSC(*args, **kwargs)

    def init_sqlq(self):
        self.sqlqueue = sqlq.SqlQueueU(server=True, db="db.db")
        self.sqlqueue.sql('''PRAGMA journal_mode=WAL;''')
        self.queue_cols = [
            "queued",
            "completed",
            "remote_root",
            "fp",
            "key",
            "md5_a",
            "remote_fp",
            "iv",
            "md5_b",
        ]
        self.sqlqueue.sql('''CREATE TABLE IF NOT EXISTS `queue` ({});'''.format(
            ", ".join("`{}` TEXT".format(_) for _ in self.queue_cols))
        )
        self.sqlqueue.commit()

    def close(self):
        if self.sqlqueue:
            self.sqlqueue.commit()
            self.sqlqueue.stop()
        self.c.close()

    def login(self, credentials = None):
        if not credentials:
            credentials = parse_credentials_argv(True)
            if credentials:
                csm.export_credentials(credentials, overwrite=True)
            else:
                credentials = csm.import_credentials()
                if not credentials:
                    credentials = [
                        input("Enter username: "),
                        getpw("Enter password: "),
                    ]
                    print()
                    csm.export_credentials(credentials)
        self.c.connect(self.ftp_domain, self.ftp_port)
        self.c.login(*credentials)
        self.c.prot_p()
        self.c.sendcmd("SYST")
        for _ in self.c.sendcmd("FEAT").splitlines():
            if "UTF8" in _:
                self.c.sendcmd("OPTS UTF8 ON")
        self.c.sendcmd("TYPE I")
        self.c.sendcmd("PASV")
        self.pwd()
        return True

    def pwd(self):
        self.cwd = self.c.pwd()
        return self.cwd

    @property
    def forbidden_characters(self):
        return "#"

    @staticmethod
    def encode_file_name(name):
        __in = "`~!@#$%^&*(    )    -_=+[{]}\\  |;:'    \"     ,<   .>   ?"
        _out = "`~!@ $%^&*&#40;&#41;-_=+[{]}\\\\|;:&#x27;&#x22;,&lt;.&gt;?"
        map = {
            "(": "&#40;",
            ")": "&#41;",
            "\\": "\\\\",
            "'": "&#x27;",
            '"': "&#x22;",
            "<": "&lt;",
            ">": "&gt;",
        }
        return re.compile("[{}]".format(re.escape("".join(list(map.keys()))))).sub(lambda k: map[k[0]], name)

    @staticmethod
    def decode_file_line(line):
        return unescape(bytes([ord(_) for _ in line]).decode())

    def parse_line_cb(self, lines: list):
        def parse_file_line(line):
            line_regex = r"^([drwx\-]+)\s+([^\s]+)\s+([A-Za-z0-9]+)\s+([A-Za-z0-9]+)\s+([0-9]+)\s+([A-Z][a-z]{2,3}\s+[0-9]+\s+[0-9]+)\s+(.*?)$"
            line = self.decode_file_line(line)
            line = re.findall(line_regex, line)[0]
            lines.append(line)

        return parse_file_line

    def change_dir(self, dir):
        self.c.cwd(dir)
        self.pwd()
        return dir

    def get_dir(self, dir: str = None):
        if dir:
            self.change_dir(dir)
        lines = []
        self.c.dir(self.parse_line_cb(lines))
        return lines

    def list_dir(self, dir: str = None):
        lines = self.get_dir(dir)
        cols = ["Permission", "?", "User", "Group", "Size", "Date", "File Name"]
        lines.insert(0, cols)
        max_col = [len(max(_, key=len)) for _ in zip(*lines)]
        tmp_cols = ["{{:>{}}}".format(_) for _ in max_col[:-1]]
        tmp_cols.append("{}")
        tmp = "  ".join(tmp_cols)
        return "\n".join(tmp.format(*line) for line in lines)

    def create_dir(self, dir: str) -> str:
        return self.c.mkd(dir)

    def get_size(self, remote_fp: str) -> int:
        return self.c.size(remote_fp)

    def raw_upload(self, fp, remote_root: str, buffer: int, cb = None, **kwargs):
        if all(_ in kwargs for _ in ["key", "iv"]):
            if isinstance(fp, str):
                fo = AESCipherCTRFileEncReader(
                    fp=fp,
                    **kwargs
                )
            else:
                fo = fp
                fp = fo.name
        else:
            if isinstance(fp, str):
                fo = open(fp, "rb")
            else:
                fo = fp
                fp = fo.name
        if self.forbidden_characters in fp:
            return print("warning: skipped '{}' due to '{}' is forbidden".format(fp, self.forbidden_characters))
        if not hasattr(fo, "read"):
            raise AttributeError(fo, "has no read()")
        fn = os.path.basename(fp)
        cmd = "STOR {}".format(fn)
        try:
            size = os.path.getsize(fp)
        except:
            size = 0
        try:
            self.change_dir(remote_root)
        except:
            self.create_dir(remote_root)
            self.change_dir(remote_root)
        remote_fp = self.encode_file_name("/".join([remote_root, fn]))
        try:
            self.get_size(remote_fp)
            self.c.delete(remote_fp)
        except:
            pass
        self.c.storbinary(cmd, fo, blocksize=buffer, callback=lambda x: callable(cb) and cb(fp, size, x))
        fo.close()

    def raw_download(self, root: str, remote_fp: str, buffer: int, cb = None, **kwargs):
        if self.forbidden_characters in remote_fp:
            return print("warning: skipped '{}' due to '{}' is forbidden".format(remote_fp, self.forbidden_characters))
        if isinstance(root, str):
            fp = os.path.join(root, *(remote_fp.split("/")[1:]))
        else:
            fp = root
        remote_fp = self.encode_file_name(remote_fp)
        if all(_ in kwargs for _ in ["key", "iv"]):
            if isinstance(fp, str):
                dir = os.path.dirname(fp)
                if dir:
                    os.makedirs(dir, exist_ok=True)
                fo = AESCipherCTRFileDecWriter(
                    fp=fp,
                    **kwargs
                )
            else:
                fo = fp
        else:
            if isinstance(fp, str):
                dir = os.path.dirname(fp)
                if dir:
                    os.makedirs(dir, exist_ok=True)
                fo = open(fp, "wb")
            else:
                fo = fp
        if not hasattr(fo, "write"):
            raise AttributeError(fo, "has no write()")
        size = self.get_size(remote_fp)
        _cb = lambda x: [fo.write(x), callable(cb) and cb(remote_fp, size, x)]
        self.c.retrbinary("RETR {}".format(remote_fp), callback=_cb, blocksize=buffer)
        fo.close()

    def download(self, root: str, remote_fp: str, buffer: int, cb = None, is_dir: bool = None, **kwargs):
        if is_dir is None:
            try:
                self.change_dir(remote_fp)
                is_dir = True
            except:
                try:
                    self.get_size(remote_fp)
                    is_dir = False
                except:
                    raise FileNotFoundError(remote_fp)
        if not is_dir:
            return self.raw_download(root, remote_fp, buffer, cb, **kwargs)
        else:
            for _ in self.get_dir(remote_fp):
                fp = remote_fp
                if fp != "/":
                    fp += "/"
                fp += _[-1]
                is_dir = _[0][0] == "d"
                self.download(root, fp, buffer, cb, is_dir, **kwargs)

    def upload_worker(self, buffer, cb):
        self.terminated = False
        while not self.terminate:
            try:
                item = self.sqlqueue.sql(
                    '''
                    SELECT `remote_root`,
                    `fp`,
                    `key`,
                    `iv`,
                    ROWID
                    FROM `queue`
                    WHERE `completed` IS NULL
                    ORDER BY ROWID
                    LIMIT 1;
                    ''',
                    (),
                    "list"
                )
                if not item:
                    break
                item = item[0]
                remote_root = item[0]
                fp = item[1]
                key = item[2]
                iv = item[3]
                kwargs = {}
                if key:
                    kwargs["key"] = key
                if iv:
                    kwargs["iv"] = b64d(iv)
                md5s = [md5(), md5()]
                if all(_ in kwargs for _ in ["key", "iv"]):
                    fo = AESCipherCTRFileEncReader(
                        fp=fp,
                        cb_before=lambda buf: md5s[0].update(buf),
                        cb_after=lambda buf: md5s[1].update(buf),
                        **kwargs
                    )
                    _cb = cb
                else:
                    fo = fp
                    def _cb(fp, size, x):
                        nonlocal md5s
                        md5s[0].update(x)
                        md5s[1] = md5s[0]
                        callable(cb) and cb(fp, size, x)
                self.raw_upload(fo, remote_root, buffer, _cb)
                self.sqlqueue.sql(
                    '''
                    UPDATE `queue`
                    SET `completed` = ?,
                    `key` = ?,
                    `md5_a` = ?,
                    `iv` = ?,
                    `md5_b` = ?
                    WHERE ROWID = ?;
                    ''',
                    (
                        dt2yyyymmddhhmmss(hms_delimiter=":"),
                        None,
                        md5s[0].hexdigest(),
                        None,
                        md5s[1].hexdigest(),
                        item[-1],
                    )
                )
                self.sqlqueue.commit()
            except:
                traceback.print_exc()
        self.terminated = True

    def queue_upload(self, *args, **kwargs):
        if not self.terminated:
            return input("cannot queue another upload")
        def job():
            buffer, cb, dry_run = self.upload(*args, queue=True, **kwargs)
            if not dry_run:
                self.upload_worker(buffer, cb)

        p = threading.Thread(target=job)
        p.daemon = True
        p.start()

    def stop_upload_worker(self):
        self.terminate = True
        while not self.terminated:
            time.sleep(1)
        self.terminate = False

    def upload(self, root, path, buffer: int, cb = None, queue: bool = False, dry_run: bool = False, **kwargs):
        if queue and not dry_run and not self.sqlqueue:
            self.init_sqlq()
        if not isinstance(path, re.Pattern):
            if path:
                if path in [".", "\\", "/"]:
                    fp = root
                else:
                    if path[0] == "." and path[1] in ["\\", "/"]:
                        path = path[2:]
                    if path[-1] in ["\\", "/"]:
                        path = path[:-1]
                    if path.startswith("Trash"):
                        raise ValueError("Trash is a reserved folder name")
                    fp = os.path.join(root, path)
            else:
                fp = root
        else:
            fp = root
        if os.path.isdir(fp):
            for a, b, c in os.walk(fp):
                b.sort()
                for d in c:
                    e = os.path.join(a, d)
                    _path = e.replace(root, "")[1:]
                    if _path.startswith("Trash"):
                        raise ValueError("Trash is a reserved folder name")
                    if isinstance(path, re.Pattern):
                        if not path.search(_path):
                            continue
                    self.upload(root, _path, buffer, cb, queue, dry_run, **kwargs)
            return buffer, cb, dry_run
        elif os.path.isfile(fp):
            remote_root = "/"+os.path.dirname(path).replace("\\", "/")
            if not queue:
                if dry_run:
                    size = os.path.getsize(fp)
                    callable(cb) and cb(fp, size, size*[None])
                else:
                    self.raw_upload(fp, remote_root, buffer, cb, **kwargs)
            else:
                try:
                    key = kwargs["key"]
                except:
                    key = None
                try:
                    iv = b64e(kwargs["iv"])
                except:
                    iv = None
                self.sqlqueue.sql(
                    '''
                        INSERT INTO `queue` VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
                    ''',
                    (
                        dt2yyyymmddhhmmss(hms_delimiter=":"),
                        None,
                        remote_root,
                        fp,
                        key,
                        None,
                        os.path.basename(path),
                        iv,
                        None,
                    )
                )
                self.sqlqueue.commit()
            return buffer, cb, dry_run



