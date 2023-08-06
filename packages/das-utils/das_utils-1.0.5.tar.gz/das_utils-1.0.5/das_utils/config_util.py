import inspect
import os
import json
import logging as log
import types


# 读取json配置文件并覆盖
def read_json(pyo: types.ModuleType, fn: str):
    """
    读取json配置文件并覆盖
    :param pyo: module
    :param fn: json配置文件绝对路径
    """
    # 获取可用属性
    d = []
    for k in pyo.__dict__:
        if not k.startswith("__"):
            if not inspect.ismodule(pyo.__dict__[k]):
                d.append(k)
    # 读取json数据
    if os.path.exists(fn):
        try:
            with open(fn) as fp:
                json_obj = json.load(fp)
        except Exception as e:
            log.error("json config failed to load:" + fn + " " + str(e))
            return
            # 覆盖数据
        for di in d:
            if di in json_obj:
                pyo.__dict__[di] = json_obj[di]
        log.info("json config has been read:" + fn)
    else:
        log.warning("json config not found:" + fn)
