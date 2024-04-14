# -*- coding: utf-8 -*-
# create by yihui 11:32 18/12/19
import logging
import os
from logging.handlers import TimedRotatingFileHandler

from src.env.EnvWrapper import env_wrapper


class LoggerWrapper:
    def __init__(self):
        self._logger = {}
        self._console_init = False

    @staticmethod
    def _get_path(action, path=""):
        """
        根据日志名，创建对应的日志路径
        :param path:
        :return:
        """
        if action != 'logs':
            action = f"logs{os.sep}{action}{os.sep}"

        path = env_wrapper.get_module_path() + os.sep + action + path
        if not os.path.exists(path):
            # 当目录不存在时，主动创建
            os.makedirs(path)

        return path

    def _gen_logger(self, path='logs', log_name='Crawler'):
        base_logger = logging.getLogger(log_name)
        base_logger.setLevel(logging.INFO)

        log_file = self._get_path(path, log_name) + os.sep + log_name + ".log"
        ch = TimedRotatingFileHandler(log_file, when='D', encoding="utf-8")
        ch.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        base_logger.addHandler(ch)
        base_logger.propagate = 0

        if env_wrapper.console_log_enable():  # and not self._console_init:
            console = logging.StreamHandler()
            console.setLevel(logging.DEBUG)
            console.setFormatter(formatter)
            base_logger.addHandler(console)
            self._console_init = True

        return base_logger

    def get_logger(self, name=None):
        if name is None:
            key = env_wrapper.get_current_task_name()
        else:
            key = name

        if key not in self._logger:
            log_name, path = key, env_wrapper.get_current_task_name()
            self._logger[key] = self._gen_logger(path, log_name)

        return self._logger[key]

    def error(self, msg, name=None):
        log = self.get_logger(name)
        log.error(msg)

    def warn(self, msg, name=None):
        log = self.get_logger(name)
        log.warning(msg)

    def info(self, msg, name=None):
        log = self.get_logger(name)
        log.info(msg)

    def debug(self, msg, name=None):
        log = self.get_logger(name)
        log.debug(msg)

    def exception(self, msg, name=None):
        """
        打印堆栈信息
        :param msg:
        :param name:
        :return:
        """
        log = self.get_logger(name)
        log.exception(msg)


SpiderLogger = LoggerWrapper()
logger = SpiderLogger.get_logger
debug = SpiderLogger.debug
info = SpiderLogger.info
error = SpiderLogger.error
warning = SpiderLogger.warn
exception = SpiderLogger.exception
