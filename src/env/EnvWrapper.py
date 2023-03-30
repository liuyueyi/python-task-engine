# -*- coding: utf-8 -*-
# create by yihui 10:48 19/9/29
import json


class EnvWrapper:
    def __init__(self):
        self._env = None
        self._log_console = False
        self._module_path = None
        self._target_task = None
        self._conf = None

    def init_env(self, env, path, task, console_log_enable=False):
        """
        初始化
        :param env: 环境，pro 表示线上，其他线下
        :param path: 项目绝对路径
        :param task: 执行的任务名
        :param console_log_enable 是否允许控制台输出日志
        :return:
        """
        self._env = env
        self._module_path = path
        self._target_task = task
        self._log_console = console_log_enable
        self.init_conf()
        print(
            f"""init env:{self._env} path:{self._module_path}, task:{self._target_task}, console:{self._log_console}, 
conf: {self._conf}""")

    def init_conf(self):
        conf_path = f"{self.get_module_path()}/conf/{'dev' if self.is_debug() else 'pro'}/app_config.json"
        with open(conf_path, "r") as reader:
            self._conf = json.loads(reader.read())
        print(f"init config : {conf_path}")

    def get_conf(self, key=None):
        if not key:
            return self._conf
        else:
            return self._conf.get(key)

    def get_module_path(self):
        return self._module_path

    def get_current_task_name(self):
        return self._target_task

    def is_debug(self):
        return not self.is_pro()

    def is_pro(self):
        return self._env == 'pro' or self._env == 'prod_hk'

    def console_log_enable(self):
        return self._log_console


env_wrapper = EnvWrapper()
