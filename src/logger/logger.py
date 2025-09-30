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
            basedir = Path(__file__).resolve().parent.parent.parent
            logs_dir = basedir / "logs"
            log_file = logs_dir / "server.log"

            logs_dir.mkdir(parents=True, exist_ok=True)

            logger = logging.getLogger('apitest')
            if not logger.handlers:
                logger.setLevel(logging.DEBUG)

                file_handler = setup_file_handler(log_file)
                logger.addHandler(file_handler)

                console_handler = setup_console_handler()
                logger.addHandler(console_handler)

            return logger
        except Exception as e:
            print(f"日志初始化失败: {e}")
            raise


# 初始化日志单例
logger = LoggerSingleton().logger