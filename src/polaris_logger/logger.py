# -*- coding: utf-8 -*-

"""
descr : 日志类封装模块
auther : lj.michale
create_date : 2025/9/27 15:54
file_name : logger.py
"""

import os
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger_formatter():
    """
    配置日志格式
    :return:
    """
    return logging.Formatter(
        '%(levelname)s %(asctime)s [%(filename)s:%(lineno)d] %(thread)d %(message)s',datefmt='%Y-%m-%d %H:%M:%S'
    )


def setup_file_handler(log_file: str):
    """
    配置文件处理器
    :param log_file:
    :return:
    作用：配置日志写入文件的规则，使用RotatingFileHandler实现日志滚动：
    maxBytes=20*1024*1024：单个日志文件最大 20MB，超过则自动切割；
    backupCount=10：最多保留 10 个历史日志文件（如server.log.1、server.log.2...）；
    encoding='utf-8'：支持中文日志正常写入。
    日志级别：setLevel(logging.DEBUG)，即文件会记录所有DEBUG及以上级别的日志（最详细）。
    """
    try:
        file_handler = RotatingFileHandler(
            log_file,
            encoding='utf-8',
            maxBytes=20 * 1024 * 1024,  # 20MB
            backupCount=10
        )
        file_handler.setFormatter(setup_logger_formatter())
        file_handler.setLevel(logging.DEBUG)
        return file_handler
    except Exception as e:
        print(f"日志文件处理器初始化失败: {e}")
        raise


def setup_console_handler():
    """
    配置控制台处理器
    :return:
    作用：配置日志在控制台的输出规则：
    输出目标：控制台（StreamHandler默认输出到stdout）；
    日志级别：setLevel(logging.INFO)，即控制台只显示INFO及以上级别（过滤掉DEBUG调试信息，避免控制台冗余）。
    """
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(setup_logger_formatter())
    console_handler.setLevel(logging.INFO)

    return console_handler


class LoggerSingleton:
    """
    日志单例类，确保整个程序中只有一个日志实例
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        __new__方法是 Python 类在实例化对象时首先调用的方法，它负责创建对象并返回该对象。通过重写__new__方法，可以控制类的实例化过程，从而实现单例模式
        :param args:
        :param kwargs:
        """
        if not cls._instance:
            cls._instance = super(LoggerSingleton, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'logger'):
            self.logger = self.init_logger()

    def init_logger(self):
        try:
            basedir = Path(__file__).resolve().parent.parent.parent # 项目根目录
            logs_dir = basedir / "logs"  # 日志目录：项目根目录/logs
            log_file = logs_dir / "server.log"  # 日志文件路径

            logs_dir.mkdir(parents=True, exist_ok=True) # 自动创建logs目录（若不存在）

            logger = logging.getLogger('apitest')  # 创建名为'apitest'的日志器
            if not logger.handlers:                # 避免重复添加处理器（防止日志重复输出）
                logger.setLevel(logging.DEBUG)     # 日志器总级别（DEBUG，允许所有级别通过）

                file_handler = setup_file_handler(log_file) # 添加文件处理器
                logger.addHandler(file_handler)             # 添加控制台处理器

                console_handler = setup_console_handler()
                logger.addHandler(console_handler)

            return logger
        except Exception as e:
            print(f"日志初始化失败: {e}")
            raise


# 初始化日志单例
logger = LoggerSingleton().logger