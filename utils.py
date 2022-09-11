import os

import json

from constants import HOME_DIR


class ConfigUtil:
    config_file_path = os.path.join(HOME_DIR, "settings.json")
    open(config_file_path, mode='a').close()

    @classmethod
    def read(cls):
        return json.loads(open(cls.config_file_path, "r").read() or "{}")

    @classmethod
    def get(cls, key):
        return cls.read().get(key)

    @classmethod
    def set(cls, key, value):
        content = cls.read()
        content[key] = value
        open(cls.config_file_path, "w").write(json.dumps(content))

    @classmethod
    def get_gitee_user_info(cls):
        return cls.get("gitee_user_info")

    @classmethod
    def set_gitee_user_info(cls, val):
        return cls.set("gitee_user_info", val)

    @classmethod
    def get_gitee_token(cls):
        return cls.get("gitee_token")

    @classmethod
    def set_gitee_token(cls, val):
        return cls.set("gitee_token", val)

    @classmethod
    def set_cache_dir(cls, val):
        return cls.set("cache_dir", val)

    @classmethod
    def get_cache_dir(cls):
        return cls.get("cache_dir")
