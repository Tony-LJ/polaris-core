# -*- coding: utf-8 -*-

"""
descr: 安全管理器，处理认证与授权
auther: lj.michale
create_date: 2025/10/23 15:54
file_name: security_manager.py
"""
# security_manager.py
import hashlib
import hmac
import time
import logging
from typing import Optional, Dict, Any
from functools import wraps
from flask import request, jsonify

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityManager:
    """
    安全管理器，处理认证与授权
    """
    def __init__(self, secret_key: str):
        """
        初始化安全管理器
        Args:
            secret_key: 密钥，用于签名验证
        """
        self.secret_key = secret_key.encode('utf-8')

    def generate_signature(self, data: str, timestamp: int) -> str:
        """
        生成签名
        Args:
            data: 待签名数据
            timestamp: 时间戳
        Returns:
            str: 生成的签名
        """
        # 构造签名内容
        sign_content = f"{data}{timestamp}".encode('utf-8')

        # 生成 HMAC-SHA256 签名
        signature = hmac.new(
            self.secret_key,
            sign_content,
            hashlib.sha256
        ).hexdigest()

        return signature

    def verify_signature(self, data: str, timestamp: int, signature: str) -> bool:
        """
        验证签名
        Args:
            data: 待验证数据
            timestamp: 时间戳
            signature: 签名
        Returns:
            bool: 签名是否有效
        """
        # 检查时间戳有效性（5分钟内有效）
        current_time = int(time.time())
        if abs(current_time - timestamp) > 300:
            logger.warning("签名时间戳已过期")
            return False
        # 生成期望的签名
        expected_signature = self.generate_signature(data, timestamp)

        # 比较签名
        return hmac.compare_digest(signature, expected_signature)

    def require_auth(self, f):
        """
        认证装饰器
        Args:
            f: 被装饰的函数
        Returns:
            装饰后的函数
        """
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # 从请求头获取认证信息
            timestamp = request.headers.get('X-Timestamp')
            signature = request.headers.get('X-Signature')
            data = request.headers.get('X-Data', '')

            # 检查必要参数
            if not all([timestamp, signature]):
                return jsonify({
                    "error": "缺少认证信息",
                    "message": "请求必须包含 X-Timestamp 和 X-Signature 头部"
                }), 401

            try:
                timestamp = int(timestamp)
            except ValueError:
                return jsonify({
                    "error": "认证信息无效",
                    "message": "X-Timestamp 必须是有效的整数"
                }), 401

            # 验证签名
            if not self.verify_signature(data, timestamp, signature):
                return jsonify({
                    "error": "认证失败",
                    "message": "签名验证失败"
                }), 401

            # 认证通过，执行原函数
            return f(*args, **kwargs)
        return decorated_function

# 创建全局安全管理器实例
# 在生产环境中，应该从安全的地方获取密钥
security_manager = SecurityManager(secret_key="your-secret-key-here")

# 使用示例
def generate_auth_headers(data: str) -> Dict[str, str]:
    """
    生成认证头部
    Args:
        data: 待签名数据

    Returns:
        Dict[str, str]: 认证头部
    """
    timestamp = int(time.time())
    signature = security_manager.generate_signature(data, timestamp)

    return {
        "X-Timestamp": str(timestamp),
        "X-Signature": signature,
        "X-Data": data
    }
