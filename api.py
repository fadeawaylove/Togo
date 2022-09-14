import json

import requests

from utils import ConfigUtil


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

    def get_user_repos(self, visibility="all", affiliation="owner", type_=None, sort="full_name", direction="asc", q="",
                       page=1, per_page=100):
        """
        获取授权用户的所有仓库
        https://gitee.com/api/v5/swagger#/getV5UserRepos
        """
        url = "https://gitee.com/api/v5/user/repos"
        params = {
            "access_token": self._secret,
        }
        return self._check_resp(requests.get(url, params))


def get_gitee_client(secret=""):
    if not secret:
        secret = ConfigUtil.get_gitee_token()
    return GiteeApi(secret)
