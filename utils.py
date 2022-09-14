import os
import threading
import json

from constants import HOME_DIR


class TaskUtil:

    def __init__(self, task_func, task_args=(), task_kw=None, callback=None, call_args=(), call_kw=None):
        self.task_func = task_func
        self.task_args = task_args
        self.task_kw = task_kw or {}
        self.callback = callback
        self.call_args = call_args
        self.call_kw = call_kw or {}

    def _run(self):
        self.task_func(*self.task_args, **self.task_kw)
        self.callback(*self.call_args, **self.call_kw)

    def run(self):
        threading.Thread(target=self._run).start()


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

    @classmethod
    def get_default_repo(cls):
        return cls.get("default_repo")

    @classmethod
    def set_default_repo(cls, val):
        return cls.set("default_repo", val)
