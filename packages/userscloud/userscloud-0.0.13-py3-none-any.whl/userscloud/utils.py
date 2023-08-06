from credsafe.utils import Manager
from functools import partial
import requests


csm = Manager("userscloud")


def create_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36"})
    s.post = partial(s.post, allow_redirects=False)
    return s


