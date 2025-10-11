# -*- coding: utf-8 -*-

"""
descr : yaml文件操作类
auther : lj.michale
create_date : 2025/10/12 15:54
file_name : yaml_handler.py
"""

import os.path
import yaml


class YamlUtil:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            print("YamlUtil first init")
            cls.__instance = super(YamlUtil, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def read_yaml(self, path):
        """
        读取yaml文件
        :param path:
        :return:
        """
        with open(path, encoding="utf-8") as f:
            result = f.read()
            result = yaml.load(result, Loader=yaml.FullLoader)
            return result

    def write_yaml(self, path, data):
        """
        写入yaml文件
        :param path:
        :param data:
        :return:
        """
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(data, f, Dumper=yaml.SafeDumper)

    # def get(self, key, default=None):
    #     """
    #     获取配置项的值
    #     :param key:
    #     :param default:
    #     :return:
    #     """
    #     return self._config.get(key, default)
    #
    # def update(self, key, value):
    #     """
    #     更新配置项的值并保存
    #     :param key:
    #     :param value:
    #     :return:
    #     """
    #     self._config[key] = value
    #     with open(self.file_path, 'w') as file:
    #         yaml.dump(self._config, file)


yamlUtil = YamlUtil()