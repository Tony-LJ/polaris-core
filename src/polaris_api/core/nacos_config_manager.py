# -*- coding: utf-8 -*-

"""
descr: Nacos 配置管理器
auther: lj.michale
create_date: 2025/10/23 15:54
file_name: nacos_config_manager.py
"""
import requests
import json
import logging
from typing import Any, Optional


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NacosConfigManager:
    """
    Nacos 配置管理器
    """
    def __init__(self, nacos_server: str = "http://localhost:8848"):
        """
        初始化配置管理器
        Args:
            nacos_server: Nacos 服务器地址
        """
        self.nacos_server = nacos_server
        self.namespace = ""  # 命名空间
        self.group = "DEFAULT_GROUP"  # 默认分组

    def publish_config(self,
                       data_id: str,
                       content: str,
                       config_type: str = "text") -> bool:
        """
        发布配置
        Args:
            data_id: 配置 ID
            content: 配置内容
            config_type: 配置类型 (text, json, xml, yaml, html, properties)
        Returns:
            bool: 发布是否成功
        """
        try:
            url = f"{self.nacos_server}/nacos/v1/cs/configs"
            # 构建请求数据
            data = {
                "dataId": data_id,
                "group": self.group,
                "content": content,
                "type": config_type
            }
            # 发送发布请求
            response = requests.post(url, data=data)
            if response.status_code == 200:
                logger.info(f"配置 {data_id} 发布成功")
                return True
            else:
                logger.error(f"配置发布失败: {response.text}")
                return False
        except Exception as e:
            logger.error(f"配置发布过程中发生错误: {str(e)}")
            return False

    def get_config(self, data_id: str) -> Optional[str]:
        """
        获取配置
        Args:
            data_id: 配置 ID
        Returns:
            str: 配置内容，如果获取失败返回 None
        """
        try:
            url = f"{self.nacos_server}/nacos/v1/cs/configs"
            # 构建请求参数
            params = {
                "dataId": data_id,
                "group": self.group
            }
            # 发送获取请求
            response = requests.get(url, params=params)
            if response.status_code == 200:
                logger.info(f"配置 {data_id} 获取成功")
                return response.text
            else:
                logger.error(f"配置获取失败: {response.text}")
                return None
        except Exception as e:
            logger.error(f"配置获取过程中发生错误: {str(e)}")
            return None

    def delete_config(self, data_id: str) -> bool:
        """
        删除配置
        Args:
            data_id: 配置 ID
        Returns:
            bool: 删除是否成功
        """
        try:
            url = f"{self.nacos_server}/nacos/v1/cs/configs"
            # 构建请求参数
            params = {
                "dataId": data_id,
                "group": self.group
            }
            # 发送删除请求
            response = requests.delete(url, params=params)
            if response.status_code == 200:
                logger.info(f"配置 {data_id} 删除成功")
                return True
            else:
                logger.error(f"配置删除失败: {response.text}")
                return False
        except Exception as e:
            logger.error(f"配置删除过程中发生错误: {str(e)}")
            return False

# 创建全局配置管理器实例
config_manager = NacosConfigManager()


if __name__ == "__main__":
    # 发布配置示例
    ai_config = {
        "model_path": "/models/ai_model.pkl",
        "max_tokens": 1024,
        "temperature": 0.7,
        "timeout": 30
    }

    success = config_manager.publish_config(
        data_id="ai-service-config",
        content=json.dumps(ai_config, indent=2),
        config_type="json"
    )

    if success:
        print("配置发布成功")
        # 获取配置
        config_content = config_manager.get_config("ai-service-config")
        if config_content:
            print(f"获取到配置: {config_content}")

            # 解析 JSON 配置
            config_data = json.loads(config_content)
            print(f"解析后的配置: {config_data}")

        # 删除配置
        config_manager.delete_config("ai-service-config")
        print("配置删除成功")
