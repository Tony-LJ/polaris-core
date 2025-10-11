# -*- coding: utf-8 -*-

from polaris_common import http_client
from polaris_common import yaml_handler
from polaris_logger import logger
from polaris_common import polaris_string_utils, date_time_utils, regex_utils


if __name__ == '__main__':
    client = http_client.HttpClient()
    status, response_text = client.get('https://h.moyanjdc.top', None)
    print(status)  # 打印HTTP状态码
    print(response_text)  # 打印响应体内容（对于requests，不需要手动关闭连接）

    config = yaml_handler.yamlUtil.read_yaml("D:\\project\\polaris-core\\docs\\application-prod.yaml")
    print(yaml_handler.yamlUtil.read_yaml("D:\\project\\polaris-core\\docs\\application-prod.yaml"))
    logger.info(yaml_handler.yamlUtil.read_yaml("D:\\project\\polaris-core\\docs\\application-prod.yaml"))
    print(polaris_string_utils.PolarisStringUtils.to_uppercase("Asdhsdjs"))
    print(polaris_string_utils.PolarisStringUtils.reverse_string("Asdhsdjs"))

    # 日期工具测试
    print(date_time_utils.DateTimeUtils.current_datetime())

    # 正则工具测试
    email = "example@example.com"
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    print(regex_utils.RegexUtils.match_pattern(pattern,email))




