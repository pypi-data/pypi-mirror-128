from requests import Request
from requests.auth import AuthBase


class Bearer(AuthBase):
    def __init__(self, token: str):
        self.token = token

    def __call__(self, r: Request):
        r.headers = {'Authorization': 'Bearer ' + self.token}
        return r
