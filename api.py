import json

import requests


class GiteeApi:

    def __init__(self, secret):
        self._secret = secret

    @staticmethod
    def _check_resp(resp, return_type="json"):
        status_code = resp.status_code
        if status_code == 200:
            content = resp.content
            if return_type == "json":
                content = json.loads(content)
            return True, content
        return False, status_code

    def get_user_info(self):
        url = "https://gitee.com/api/v5/user"
        res = requests.get(url, params={"access_token": self._secret})
        return self._check_resp(res)
