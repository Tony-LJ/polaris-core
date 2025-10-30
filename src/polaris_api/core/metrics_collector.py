# -*- coding: utf-8 -*-

"""
descr: 服务监控与追踪
auther: lj.michale
create_date: 2025/10/23 15:54
file_name: metrics_collector.py
"""
import time
import logging
from typing import Dict, Any
from collections import defaultdict

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MetricsCollector:
    """
    指标收集器，用于收集服务运行指标
    """
    def __init__(self):
        """
        初始化指标收集器
        """
        self.metrics = defaultdict(int)
        self.request_times = []
        self.start_time = time.time()

    def increment_counter(self, metric_name: str, value: int = 1):
        """
        增加计数器
        Args:
            metric_name: 指标名称
            value: 增加的值
        """
        self.metrics[metric_name] += value
        logger.debug(f"指标 {metric_name} 增加 {value}，当前值: {self.metrics[metric_name]}")

    def record_request_time(self, duration: float):
        """
        记录请求耗时
        Args:
            duration: 请求耗时（秒）
        """
        self.request_times.append(duration)
        logger.debug(f"记录请求耗时: {duration:.4f}秒")

    def get_metrics(self) -> Dict[str, Any]:
        """
        获取当前指标
        Returns:
            Dict[str, Any]: 指标数据
        """
        # 计算平均请求时间
        avg_request_time = 0
        if self.request_times:
            avg_request_time = sum(self.request_times) / len(self.request_times)
        # 计算运行时间
        uptime = time.time() - self.start_time

        return {
            "counters": dict(self.metrics),
            "avg_request_time": avg_request_time,
            "total_requests": len(self.request_times),
            "uptime": uptime
        }

# 创建全局指标收集器实例
metrics_collector = MetricsCollector()

# 装饰器用于自动收集指标
def collect_metrics(func):
    """
    装饰器，用于自动收集函数执行指标
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            # 执行函数
            result = func(*args, **kwargs)
            # 记录成功指标
            metrics_collector.increment_counter(f"{func.__name__}_success")
            return result
        except Exception as e:
            # 记录失败指标
            metrics_collector.increment_counter(f"{func.__name__}_failure")
            raise
        finally:
            # 记录执行时间
            duration = time.time() - start_time
            metrics_collector.record_request_time(duration)
            metrics_collector.increment_counter(f"{func.__name__}_total")
    return wrapper

# 使用示例
@collect_metrics
def example_ai_prediction(data):
    """
    示例 AI 预测函数
    """
    # 模拟处理时间
    time.sleep(0.1)
    # 模拟预测逻辑
    return {"result": "positive", "confidence": 0.95}

# 指标接口
def get_service_metrics():
    """
    获取服务指标接口
    """
    return metrics_collector.get_metrics()
