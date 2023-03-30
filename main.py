# -*- coding: utf-8 -*-
# create by yihui 10:45 20/2/18

import asyncio
import getopt
import importlib
import logging
import os
import sys

from src.env.EnvWrapper import env_wrapper
from src.plugins.PluginHolder import plugin_holder
from src.plugins.http.ProxyManager import init_proxy
from src.plugins.logger.LoggerWrapper import SpiderLogger


def get_path():
    """
    获取项目根路径
    :return:
    """
    # 支持linux、win系统的路径切换
    return os.path.abspath(__file__).replace("/main.py", "").replace("\\main.py", "")


def gen_task(task_name):
    """
    根据任务名称自动映射到对应的任务上
        * 任务名和类名必须一样
    """
    target_name = f'{task_name}.py'
    app_path = get_path()
    for i in os.walk(f'{app_path}/src/biz'):
        if target_name in i[-1]:
            model_path = f'{i[0].replace(app_path, "").replace("/", ".").strip(".")}.{task_name}'
            task_instance = importlib.import_module(model_path)
            _ = task_instance
            return eval(f'task_instance.{task_name}()')

    raise Exception(f"no modle: {task_name} found!")


async def init_and_run(env, use_proxy, console_log, action_name):
    abs_path = get_path()
    env_wrapper.init_env(env, abs_path, action_name, console_log)
    if use_proxy:
        init_proxy(use_proxy)
    SpiderLogger.debug(f'Current Env: {env}, module: {abs_path}, task: {action_name}', 'core')
    target_task = gen_task(action_name)
    SpiderLogger.debug(f"启动任务: {action_name}", "core")
    await target_task.async_init()
    result = await target_task.call()
    SpiderLogger.debug(f"执行完毕: {action_name}, {result}", "core")


async def main(action_name, args):
    opts, args = getopt.getopt(args, "i:r:w:t:q:e:p:o:s:l",
                               ['interval:', 'crawler:', 'washer:', 'target:', 'quantity:',
                                'env:', 'proxy:', 'timeout:', 'script:', 'log:'])

    # 工作环境
    work_env = 'dev'
    # 是否控制台输出日志
    console_log = False
    # 默认超时时间
    timeout = None
    use_proxy = None
    for opt, arg in opts:
        if opt in ('-e', '--env'):
            work_env = arg
            assert work_env in ['local', 'dev', 'pro', 'prod_hz', 'prod_hk'], "工作环境错误"
        if opt in ('-p', '--proxy'):
            use_proxy = arg
            assert use_proxy in ['socks', 'fixed', 'no_proxy'], "代理方式选择错误"
        if opt in ('-l', '--log'):
            # 表示日志除了打印文件之外，也打印一份到控制台
            console_log = True
        if opt in ('-o', '--timeout'):
            # 超时
            try:
                timeout = int(arg)
            except ValueError:
                print("请指定正确的超时时间")
        if opt in ('-i', '--interval'):
            try:
                cycle_execution = arg
            except ValueError:
                print("请指定正确的循环间歇时间")
                raise getopt.GetoptError

    # 初始化并执行任务
    await init_and_run(work_env, use_proxy, console_log, action_name)
    # 回收资源
    await asyncio.wait_for(plugin_holder.release(), timeout=timeout)


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main(sys.argv[1], sys.argv[2:]))
        loop.close()
    except InterruptedError as e:
        logging.error("some error: ", e)
