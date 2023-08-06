from .helper import UC
from .utils import create_session


class UC_API(UC):
    def __init__(self, *, key: str, debug: bool = False):
        super().__init__(debug=debug)
        self.s = create_session()
        self.url = self.domain+"/api/{{}}/{{}}?key={}".format(key)

    def AccountInfo(self):
        args = [_ for _ in (None, ) if _]
        url = self.url.format("account", "info")+("&"+"".join(args) if args else "")
        r = self.s.get(url)
        if self.debug:
            print("AccountInfo", url)
        if r.status_code != 200:
            raise Exception("failed to perform AccountInfo due to status code '{}'\n{}".format(r.status_code, r.content.decode()))
        return r.json()

    def AccountStats(self, last: int = 7):
        args = [_ for _ in (None, "last={}".format(last) if last is not None else None) if _]
        url = self.url.format("account", "stats")+("&"+"".join(args) if args else "")
        r = self.s.get(url)
        if self.debug:
            print("AccountStats", url)
        if r.status_code != 200:
            raise Exception("failed to perform AccountStats due to status code '{}'\n{}".format(r.status_code, r.content.decode()))
        return r.json()

    def UploadServer(self):
        args = [_ for _ in (None, ) if _]
        url = self.url.format("upload", "server")+("&"+"".join(args) if args else "")
        r = self.s.get(url)
        if self.debug:
            print("UploadServer", url)
        if r.status_code != 200:
            raise Exception("failed to perform UploadServer due to status code '{}'\n{}".format(r.status_code, r.content.decode()))
        return r.json()

    def FileInfo(self, file_code: str):
        args = [_ for _ in (None, "file_code={}".format(file_code) if file_code is not None else None) if _]
        url = self.url.format("file", "info")+("&"+"".join(args) if args else "")
        r = self.s.get(url)
        if self.debug:
            print("FileInfo", url)
        if r.status_code != 200:
            raise Exception("failed to perform FileInfo due to status code '{}'\n{}".format(r.status_code, r.content.decode()))
        return r.json()

    def FileList(self, page: int = 1, per_page: int = 20, fld_id: int = 0, public: int = None, created: str = None, name: str = None):
        args = [_ for _ in (None, "page={}".format(page) if page is not None else None, "per_page={}".format(per_page) if per_page is not None else None, "fld_id={}".format(fld_id) if fld_id is not None else None, "public={}".format(public) if public is not None else None, "created={}".format(created) if created is not None else None, "name={}".format(name) if name is not None else None) if _]
        url = self.url.format("file", "list")+("&"+"".join(args) if args else "")
        r = self.s.get(url)
        if self.debug:
            print("FileList", url)
        if r.status_code != 200:
            raise Exception("failed to perform FileList due to status code '{}'\n{}".format(r.status_code, r.content.decode()))
        return r.json()

    def FileRename(self, file_code: str, name: str):
        args = [_ for _ in (None, "file_code={}".format(file_code) if file_code is not None else None, "name={}".format(name) if name is not None else None) if _]
        url = self.url.format("file", "rename")+("&"+"".join(args) if args else "")
        r = self.s.get(url)
        if self.debug:
            print("FileRename", url)
        if r.status_code != 200:
            raise Exception("failed to perform FileRename due to status code '{}'\n{}".format(r.status_code, r.content.decode()))
        return r.json()

    def FileClone(self, file_code: str):
        args = [_ for _ in (None, "file_code={}".format(file_code) if file_code is not None else None) if _]
        url = self.url.format("file", "clone")+("&"+"".join(args) if args else "")
        r = self.s.get(url)
        if self.debug:
            print("FileClone", url)
        if r.status_code != 200:
            raise Exception("failed to perform FileClone due to status code '{}'\n{}".format(r.status_code, r.content.decode()))
        return r.json()

    def FileSetFolder(self, file_code: str, fld_id: int):
        args = [_ for _ in (None, "file_code={}".format(file_code) if file_code is not None else None, "fld_id={}".format(fld_id) if fld_id is not None else None) if _]
        url = self.url.format("file", "set_folder")+("&"+"".join(args) if args else "")
        r = self.s.get(url)
        if self.debug:
            print("FileSetFolder", url)
        if r.status_code != 200:
            raise Exception("failed to perform FileSetFolder due to status code '{}'\n{}".format(r.status_code, r.content.decode()))
        return r.json()

    def FolderList(self, fld_id: int):
        args = [_ for _ in (None, "fld_id={}".format(fld_id) if fld_id is not None else None) if _]
        url = self.url.format("folder", "list")+("&"+"".join(args) if args else "")
        r = self.s.get(url)
        if self.debug:
            print("FolderList", url)
        if r.status_code != 200:
            raise Exception("failed to perform FolderList due to status code '{}'\n{}".format(r.status_code, r.content.decode()))
        return r.json()

    def CreateFolder(self, parent_id: int, name: str):
        args = [_ for _ in (None, "parent_id={}".format(parent_id) if parent_id is not None else None, "name={}".format(name) if name is not None else None) if _]
        url = self.url.format("folder", "create")+("&"+"".join(args) if args else "")
        r = self.s.get(url)
        if self.debug:
            print("CreateFolder", url)
        if r.status_code != 200:
            raise Exception("failed to perform CreateFolder due to status code '{}'\n{}".format(r.status_code, r.content.decode()))
        return r.json()

    def RenameFolder(self, fld_id: int, name: str):
        args = [_ for _ in (None, "fld_id={}".format(fld_id) if fld_id is not None else None, "name={}".format(name) if name is not None else None) if _]
        url = self.url.format("folder", "rename")+("&"+"".join(args) if args else "")
        r = self.s.get(url)
        if self.debug:
            print("RenameFolder", url)
        if r.status_code != 200:
            raise Exception("failed to perform RenameFolder due to status code '{}'\n{}".format(r.status_code, r.content.decode()))
        return r.json()

    def DeletedFiles(self, last: int = 20):
        args = [_ for _ in (None, "last={}".format(last) if last is not None else None) if _]
        url = self.url.format("files", "deleted")+("&"+"".join(args) if args else "")
        r = self.s.get(url)
        if self.debug:
            print("DeletedFiles", url)
        if r.status_code != 200:
            raise Exception("failed to perform DeletedFiles due to status code '{}'\n{}".format(r.status_code, r.content.decode()))
        return r.json()

    def DMCAFiles(self, last: int = 20):
        args = [_ for _ in (None, "last={}".format(last) if last is not None else None) if _]
        url = self.url.format("files", "dmca")+("&"+"".join(args) if args else "")
        r = self.s.get(url)
        if self.debug:
            print("DMCAFiles", url)
        if r.status_code != 200:
            raise Exception("failed to perform DMCAFiles due to status code '{}'\n{}".format(r.status_code, r.content.decode()))
        return r.json()








