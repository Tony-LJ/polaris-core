# -*- coding: utf-8 -*-

from polaris_common import http_client
from polaris_common import yaml_handler
from polaris_logger import logger

if __name__ == '__main__':
    client = http_client.HttpClient()
    status, response_text = client.get('https://h.moyanjdc.top', None)
    print(status)  # 打印HTTP状态码
    print(response_text)  # 打印响应体内容（对于requests，不需要手动关闭连接）

    print(yaml_handler.yamlUtil.read_yaml("D:\\project\\polaris-core\\docs\\application-prod.yaml"))
    logger.info(yaml_handler.yamlUtil.read_yaml("D:\\project\\polaris-core\\docs\\application-prod.yaml"))


