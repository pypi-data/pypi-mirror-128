from omnitools import sha3_512hd, parse_credentials_argv, getpw
from .utils import create_session, csm
from .helper import UC
from lxml import html
import random
import re
import os


class UC_WEB(UC):
    s = create_session()
    token: str = None
    fld_id: str = None
    ROOT: int = 0
    remote_upload_kill_url: str = None
    remote_upload_progress_url: str = None

    def register(self, credentials, email: str):
        r = self.s.get(self.domain+"/register.html")
        r = html.fromstring(r.content.decode())
        form = r.xpath("//*[@name='token']/..")[0]
        op = form.xpath(".//input[@name='op']/@value")[0]
        save = form.xpath(".//input[@name='save']/@value")[0]
        rand = form.xpath(".//input[@name='rand']/@value")[0]
        token = form.xpath(".//input[@name='token']/@value")[0]
        codes = form.xpath(".//*[@name='token']/..//table//td/div/span")
        code = []
        for _ in codes:
            code.append([_.xpath("./text()")[0], int(_.xpath("./@style")[0].split("left:")[1].split("px")[0])])
        code.sort(key=lambda x: x[1])
        code = "".join(_[0] for _ in code)
        data = {
            "op": op,
            "save": save,
            "rand": rand,
            "token": token,
            "next": "",
            "usr_login": credentials[0],
            "usr_email": email,
            "usr_password": credentials[1],
            "usr_password2": credentials[1],
            "code": code,
        }
        r = self.s.post(self.domain+"/register.html", data=data)
        r = html.fromstring(r.content.decode())
        alert = r.xpath("//*[contains(@class, 'alert-danger')]//text()")
        if alert:
            raise Exception(alert[-1].strip())
        return input("register complete. please check your email for activation. press enter to continue... ")

    def delete_all_sessions(self):
        data = {
            "op": "my_account",
        }
        r = self.s.get(self.domain, params=data, allow_redirects=False)
        r = html.fromstring(r.content.decode())
        hrefs = r.xpath("//a[contains(@href, 'del_session')]/@href")
        for href in hrefs:
            r = self.s.get(self.domain+"/"+href, allow_redirects=False)
            if self.debug:
                print("delete_all_sessions", r.status_code, len(r.content.decode()))
            if r.status_code != 302:
                raise Exception("cannot delete all sessions due to status code '{}'\n{}".format(r.status_code, r.content.decode()))

    def get_api_key(self):
        data = {
            "op": "my_account",
        }
        r = self.s.get(self.domain, params=data, allow_redirects=False)
        if self.debug:
            print("get_api_key", r.status_code, len(r.content.decode()))
        if r.status_code != 200:
            raise Exception("cannot get api key due to status code '{}'\n{}".format(r.status_code, r.content.decode()))
        r = html.fromstring(r.content.decode())
        api_key = r.xpath("//div[contains(@class, 'item')]/div[@class='row'][3]//input[1]/@value")[0]
        if re.search(r"^[a-z0-9]+$", api_key):
            return api_key
        else:
            return None

    def change_api_key(self):
        data = {
            "op": "my_account",
        }
        r = self.s.get(self.domain, params=data, allow_redirects=False)
        r = html.fromstring(r.content.decode())
        href = r.xpath("//a[contains(@href, 'api_key')]/@href")[0]
        r = self.s.get(self.domain+"/"+href, allow_redirects=False)
        if self.debug:
            print("change_api_key", r.status_code, r.content.decode())
        if r.status_code != 302:
            raise Exception("cannot change api key due to status code '{}'\n{}".format(r.status_code, r.content.decode()))

    def login(self, credentials = None):
        if self.debug:
            print("logging in")
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
        self.s.get(self.domain)
        self.s.post(self.domain, data={
            "op": "login",
            "login": credentials[0],
            "password": credentials[1],
        })
        r = self.s.get(self.domain, params={
            "op": "my_files"
        })
        r = html.fromstring(r.content.decode())
        try:
            username = "".join(r.xpath("//li[contains(@class, 'user')]/a/text()")).strip()
            if credentials[0] != username:
                raise
            self.hash = sha3_512hd(sha3_512hd(sha3_512hd(credentials[1])))
        except:
            raise Exception("cannot login, please check your credentials")
        self.token = r.xpath("//input[@name='token']/@value")[0]
        if self.debug:
            print("logged in")

    def get_trash(self):
        data = {
            "op": "my_files",
            "fld_id": -1,
        }
        r = self.s.get(self.domain, params=data)
        if self.debug:
            print("get_trash", data, r.status_code, len(r.content))
        if r.status_code != 200:
            raise Exception("cannot get folder '{}' due to status code '{}'\n{}".format(dir, r.status_code, r.content.decode()))
        r = html.fromstring(r.content.decode())
        FileContent = r.xpath("//*[@id='FileContent']")[0]
        names = FileContent.xpath(".//*[@id='files_list']//tr")
        list = []
        for _ in names:
            links = _.xpath(".//a/@href")
            links = [_.replace(self.domain, "") for _ in links]
            links = [_[1:] if _[0] == "/" else _ for _ in links if _]
            links = [dict(re.findall(r"(?:\?|&)([^=]+)=([^&]+)", _)) if _[0] == "?" else _ for _ in links]
            if links:
                name = _.xpath(".//b//text()")[0].strip()
                if name == "Trash":
                    continue
                links.insert(0, name)
                list.append(links)
        return list

    def list_trash(self):
        return "\n".join(_[0] for _ in self.get_trash())

    def restore_file(self, file: int):
        data = {
            "op": "my_files",
            "token": self.token,
            "file_id": file,
            "untrash_selected": "1",
        }
        r = self.s.get(self.domain, params=data, allow_redirects=False)
        if self.debug:
            print("restore_file", data, r.status_code, r.content.decode())
        if r.status_code != 302:
            raise Exception("cannot restore file '{}' due to status code '{}'\n{}".format(file, r.status_code, r.content.decode()))

    def get_all_folders(self):
        data = {
            "op": "my_files",
            "fld_id": 0,
        }
        r = self.s.get(self.domain, params=data)
        if self.debug:
            print("get_all_folders", data, r.status_code, len(r.content))
        if r.status_code != 200:
            raise Exception("cannot get all folders due to status code '{}'\n{}".format(r.status_code, r.content.decode()))
        r = html.fromstring(r.content.decode())
        folders = [[
            _.xpath("./@value")[0],
            _.xpath("./text()")[0].strip(),
            _.xpath("./text()")[0].count(b"\xc2\xa0".decode())//2,
        ] for _ in r.xpath("//*[@name='to_folder']/option[@value]")]
        return folders

    def get_folder(self, dir: int):
        data = {
            "op": "my_files",
            "fld_id": dir,
        }
        r = self.s.get(self.domain, params=data)
        if self.debug:
            print("get_folder", data, r.status_code, len(r.content))
        if r.status_code != 200:
            raise Exception("cannot get folder '{}' due to status code '{}'\n{}".format(dir, r.status_code, r.content.decode()))
        r = html.fromstring(r.content.decode())
        FileContent = r.xpath("//*[@id='FileContent']")[0]
        list = [[], []]
        for i, name in enumerate(["folders", "files"]):
            names = FileContent.xpath(".//*[@id='{}_list']//tr".format(name))
            for _ in names:
                links = _.xpath(".//a/@href")
                if i == 0:
                    links = [
                        dict(re.findall(r"(?:\?|&)([^=]+)=([^&]+)", _)) for _ in links if _[0] == "?"
                    ]
                else:
                    links = [dict(re.findall(r"(?:\?|&)([^=]+)=([^&]+)", _)) if _[0] == "?" else _ for _ in links if "&sort" not in _ and (_.count("/") == 3 or _[0] == "?")]
                    if links:
                        file_id = _.xpath(".//*[@name='file_id']/@value")[0]
                        links.insert(0, file_id)
                if links:
                    name = _.xpath(".//b//text()")[0].strip()
                    if name == "Trash":
                        continue
                    links.insert(0, name)
                    list[i].append(links)
        return list

    def list_folder(self, dir: int):
        folders, files = self.get_folder(dir)
        return "\n".join(_[0] for _ in folders+files)

    def create_new_folder(self, base: int, name: str):
        if name == "Trash":
            raise NameError("'Trash' is a reserved name.")
        data = {
            "op": "my_files",
            "token": self.token,
            "fld_id": base,
            "create_new_folder": name,
        }
        r = self.s.post(self.domain, data=data)
        if self.debug:
            print("create_new_folder", data, r.status_code, r.content.decode())
        if r.status_code != 302:
            raise Exception("cannot create new folder '{}' at '{}' due to status code '{}'\n{}".format(name, base, r.status_code, r.content.decode()))

    def delete_folder(self, base: int, dir: int):
        data = {
            "op": "my_files",
            "token": self.token,
            "fld_id": base,
            "del_folder": dir,
        }
        r = self.s.get(self.domain, params=data, allow_redirects=False)
        if self.debug:
            print("delete_folder", data, r.status_code, r.content.decode())
        if r.status_code != 302:
            raise Exception("cannot delete folder '{}' from '{}' due to status code '{}'\n{}".format(base, dir, r.status_code, r.content.decode()))

    def delete_file(self, del_code: str):
        data = {
            "op": "my_files",
            "token": self.token,
            "del_code": del_code,
        }
        r = self.s.get(self.domain, params=data, allow_redirects=False)
        if self.debug:
            print("delete_file", data, r.status_code, r.content.decode())
        if r.status_code != 302:
            raise Exception("cannot delete file '{}' due to status code '{}'\n{}".format(del_code, r.status_code, r.content.decode()))

    def edit_folder(self, dir: int, name: str = "", desc: str = ""):
        if name == "Trash":
            raise NameError("'Trash' is a reserved name.")
        if not name and not desc:
            return
        params = {
            "op": "fld_edit",
            "fld_id": dir,
        }
        r = self.s.get(self.domain, params=params)
        r = html.fromstring(r.content.decode())
        data = {
            "op": "fld_edit",
            "token": r.xpath("//input[@name='token']/@value")[0],
            "fld_id": dir,
            "fld_name": name or r.xpath("//input[@name='fld_name']/@value")[0],
            "fld_descr": desc or r.xpath("//input[@name='fld_descr']/@value")[0],
            "save": " Submit ",
        }
        r = self.s.post(self.domain, params=params, data=data)
        if self.debug:
            print("edit_folder", data, r.status_code, r.content.decode())
        if r.status_code != 302:
            raise Exception("cannot edit folder '{}' '{}' '{}' due to status code '{}'\n{}".format(dir, name, desc, r.status_code, r.content.decode()))

    def edit_file(self, code: str, name: str = "", desc: str = "", password: str = ""):
        if not name and not desc and not password:
            return
        params = {
            "op": "file_edit",
            "file_code": code,
        }
        r = self.s.get(self.domain, params=params)
        r = html.fromstring(r.content.decode())
        data = {
            "op": "file_edit",
            "token": r.xpath("//input[@name='token']/@value")[0],
            "file_id": r.xpath("//input[@name='file_id']/@value")[0],
            "file_name": name or r.xpath("//input[@name='file_name']/@value")[0],
            "file_descr": desc or "\n".join(r.xpath("//textarea[@name='file_descr']/text()")),
            "file_password": password or r.xpath("//input[@name='file_password']/@value")[0],
            "save": " Submit ",
        }
        r = self.s.post(self.domain, params=params, data=data)
        if self.debug:
            print("edit_file", data, r.status_code, r.content.decode())
        if r.status_code != 302:
            raise Exception("cannot edit file '{}' '{}' '{}' due to status code '{}'\n{}".format(code, name, desc, r.status_code, r.content.decode()))

    def copy_file(self, file: int, src_dir: int, dst_dir: int):
        data = {
            "op": "my_files",
            "token": self.token,
            "fld_id": src_dir,
            "file_id": file,
            "to_folder": dst_dir,
            "to_folder_copy": "Copy files",
        }
        r = self.s.post(self.domain, data=data)
        if self.debug:
            print("copy_file", data, r.status_code, r.content.decode())
        if r.status_code != 302:
            raise Exception("cannot copy file '{}' from '{}' to '{}' due to status code '{}'\n{}".format(file, src_dir, dst_dir, r.status_code, r.content.decode()))

    def move_file(self, file: int, src_dir: int, dst_dir: int):
        data = {
            "op": "my_files",
            "token": self.token,
            "fld_id": src_dir,
            "file_id": file,
            "to_folder": dst_dir,
            "to_folder_move": "Mopy files",
        }
        r = self.s.post(self.domain, data=data)
        if self.debug:
            print("move_file", data, r.status_code, r.content.decode())
        if r.status_code != 302:
            raise Exception("cannot move file '{}' from '{}' to '{}' due to status code '{}'\n{}".format(file, src_dir, dst_dir, r.status_code, r.content.decode()))

    def logout(self):
        if self.debug:
            print("logging out")
        self.s.get(self.domain, params={
            "op": "logout"
        })
        if self.debug:
            print("logged out")

    def upload_file(self, base: int, fp: str, recipient: str = "", password: str = ""):
        if os.path.isdir(fp):
            raise IsADirectoryError(fp)
        if not os.path.isfile(fp):
            raise FileNotFoundError(fp)
        r = self.s.get(self.domain)
        r = html.fromstring(r.content.decode())
        form = r.xpath("//*[@id='uploadfile']")[0]
        url = form.xpath("./@action")[0]
        sess_id = form.xpath(".//input[@name='sess_id']/@value")[0]
        utype = form.xpath(".//input[@name='utype']/@value")[0]
        data = {
            "sess_id": sess_id,
            "utype": utype,
            "to_folder": base,
            "link_rcpt": recipient,
            "link_pass": password,
            # "keepalive": "1",
        }
        r = self.s.post(url, data=data, files={"file_0": open(fp, "rb")})
        if self.debug:
            print("upload_file", data, r.status_code, r.content.decode())
        if r.status_code != 200:
            raise Exception("cannot upload '{}' to '{}' due to status code '{}'\n{}".format(fp, base, r.status_code, r.content.decode()))
        return self.domain+"/"+r.json()[0]["file_code"]

    def upload_remote_url(self, base: int, remote_url: str, recipient: str = "", password: str = "", proxyurl: str = ""):
        r = self.s.get(self.domain)
        r = html.fromstring(r.content.decode())
        form = r.xpath("//*[@id='uploadurl']")[0]
        url = form.xpath("./@action")[0]
        job_id = "".join(str(random.randint(0, 9)) for _ in range(0, 12))
        self.remote_upload_kill_url = url + "&kill=" + job_id
        self.remote_upload_progress_url = "https://cloud0.userscloud.com/tmp/" + job_id + ".json"
        url += "&upload_id="+job_id
        sess_id = form.xpath(".//input[@name='sess_id']/@value")[0]
        utype = form.xpath(".//input[@name='utype']/@value")[0]
        file_public = form.xpath(".//input[@name='file_public']/@value")[0]
        data = {
            "sess_id": sess_id,
            "utype": utype,
            "url_mass": remote_url,
            "to_folder": base,
            "recemail": recipient,
            "linkpass": password,
            "proxyurl": proxyurl,
            # "keepalive": "1",
            "tos": "",
            "file_public": file_public,
        }
        r = self.s.post(url, data=data)
        if self.debug:
            print("upload_remote_url", data, r.status_code, r.content.decode())
        if r.status_code != 200:
            raise Exception("cannot remote upload url '{}' to '{}' due to status code '{}'\n{}".format(url, base, r.status_code, r.content.decode()))
        return self.domain+"/"+r.json()[0]["file_code"]

    def upload_copy_url(self, uc_url: str):
        data = {
            "op": "my_files",
            "add_my_acc": "1",
            "token": self.token,
            "url_mass": uc_url,
            "upload": "",
            "tos": "",
        }
        r = self.s.post(self.domain, data=data)
        if self.debug:
            print("upload_copy_url", data, r.status_code, len(r.content))
        if r.status_code != 200:
            raise Exception("cannot remote copy url '{}' due to status code '{}'\n{}".format(uc_url, r.status_code, r.content.decode()))
        return [self.domain+"/"+_ for _ in re.findall(r"value=.(?!upload)([a-z0-9]+)", r.content.decode())]



