# -*- coding: utf-8 -*-

"""
descr: nacos client
auther: lj.michale
create_date: 2025/10/23 15:54
file_name: nacos_client.py
"""

import requests
import json
import logging
from typing import Dict, Any

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NacosClient:
    """
    Nacos 客户端，用于服务注册与发现
    """
    def __init__(self,
                 nacos_server: str = "http://localhost:8848"):
        """
        初始化 Nacos 客户端
        Args:
            nacos_server: Nacos 服务器地址
        """
        self.nacos_server = nacos_server
        self.namespace = ""  # 命名空间，可以为空
        self.group = "DEFAULT_GROUP"  # 默认分组

    def register_service(self,
                         service_name: str,
                         ip: str,
                         port: int,
                         metadata: Dict[str, Any] = None) -> bool:
        """
        注册服务到 Nacos
        Args:
            service_name: 服务名称
            ip: 服务 IP 地址
            port: 服务端口
            metadata: 服务元数据
        Returns:
            bool: 注册是否成功
        """
        try:
            url = f"{self.nacos_server}/nacos/v1/ns/instance"
            # 构建请求参数
            params = {
                "serviceName": service_name,
                "ip": ip,
                "port": port,
                "groupName": self.group
            }
            # 添加元数据
            if metadata:
                params["metadata"] = json.dumps(metadata)
            # 发送注册请求
            response = requests.post(url, params=params)
            if response.status_code == 200:
                logger.info(f"服务 {service_name} 注册成功")
                return True
            else:
                logger.error(f"服务注册失败: {response.text}")
                return False
        except Exception as e:
            logger.error(f"服务注册过程中发生错误: {str(e)}")
            return False

    def deregister_service(self, service_name: str, ip: str, port: int) -> bool:
        """
        从 Nacos 注销服务
        Args:
            service_name: 服务名称
            ip: 服务 IP 地址
            port: 服务端口
        Returns:
            bool: 注销是否成功
        """
        try:
            url = f"{self.nacos_server}/nacos/v1/ns/instance"
            # 构建请求参数
            params = {
                "serviceName": service_name,
                "ip": ip,
                "port": port,
                "groupName": self.group
            }
            # 发送注销请求
            response = requests.delete(url, params=params)
            if response.status_code == 200:
                logger.info(f"服务 {service_name} 注销成功")
                return True
            else:
                logger.error(f"服务注销失败: {response.text}")
                return False
        except Exception as e:
            logger.error(f"服务注销过程中发生错误: {str(e)}")
            return False

    def get_service_instances(self, service_name: str) -> list:
        """
        获取服务实例列表
        Args:
            service_name: 服务名称
        Returns:
            list: 服务实例列表
        """
        try:
            url = f"{self.nacos_server}/nacos/v1/ns/instance/list"
            # 构建请求参数
            params = {
                "serviceName": service_name,
                "groupName": self.group
            }
            # 发送查询请求
            response = requests.get(url, params=params)

            if response.status_code == 200:
                data = response.json()
                instances = data.get("hosts", [])
                logger.info(f"获取到 {len(instances)} 个服务实例")
                return instances
            else:
                logger.error(f"获取服务实例失败: {response.text}")
                return []

        except Exception as e:
            logger.error(f"获取服务实例过程中发生错误: {str(e)}")
            return []

# 创建全局 Nacos 客户端实例
nacos_client = NacosClient()



if __name__ == "__main__":
    # 注册服务示例
    success = nacos_client.register_service(
        service_name="ai-service",
        ip="127.0.0.1",
        port=5000,
        metadata={
            "version": "1.0.0",
            "description": "AI 预测服务"
        }
    )

    if success:
        print("服务注册成功")

        # 获取服务实例
        instances = nacos_client.get_service_instances("ai-service")
        print(f"服务实例: {instances}")

        # 注销服务
        nacos_client.deregister_service("ai-service", "127.0.0.1", 5000)
        print("服务注销成功")


