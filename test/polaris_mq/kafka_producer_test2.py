# -*- coding: utf-8 -*-

import json
import kafka

class KProducer(object):
    """
    kafka 的生产者模型
    """

    _coding = "utf-8"

    def __init__(self,
                 broker='10.53.0.73:9092,10.53.0.74:9092,10.53.0.75:9092',
                 topic="kw-sync",
                 max_request_size=104857600,
                 batch_size=0,  # 即时发送,提高并发可以适当增加,但是会造成消息的延迟;
                 **kwargs):
        """
        初始化设置 kafka 生产者连接对象;参数不存在的情况下使用配置文件中的默认连接;
        """
        self.broker = broker
        self.topic = topic
        self.max_request_size = max_request_size
        # 实例化生产者对象
        self.producer_json = kafka.KafkaProducer(
            bootstrap_servers=self.broker,
            max_request_size=self.max_request_size,
            batch_size=batch_size,
            key_serializer=lambda k: json.dumps(k).encode(self._coding),  # 设置键的形式使用匿名函数进行转换
            value_serializer=lambda v: json.dumps(v).encode(self._coding),  # 当需要使用 json 传输地时候必须加上这两个参数
            **kwargs
        )

        self.producer = kafka.KafkaProducer(
            bootstrap_servers=broker,
            max_request_size=self.max_request_size,
            batch_size=batch_size,
            api_version=(0, 10, 1),
            **kwargs
        )

    def send(self, message: bytes, partition: int = 0):
        """
        写入普通的消息;
        Args:
            message: bytes; 字节流数据;将字符串编码成 utf-8的格式;
            partition: int; kafka 的分区,将消息发送到指定的分区之中;
        Returns:
            None
        """
        future = self.producer.send(self.topic, message, partition=partition)
        record_metadata = future.get(timeout=30)
        if future.failed():  # 发送失败,记录异常到日志;
            raise Exception("send message failed:%s)" % future.exception)

    def send_json(self, key: str, value: dict, partition: int = 0):
        """
        发送 json 形式的数据;
        Args:
            key: str; kafka 中键的值
            value: dict; 发送的具体消息
            partition: int; 分区的信息
        Returns:
            None
        """
        future = self.producer_json.send(self.topic, key=key, value=value, partition=partition)
        record_metadata = future.get(timeout=30)
        if future.failed():  # 发送失败记录异常;
            raise Exception("send json message failed:%s)" % future.exception)

    def close(self):
        """
        关闭kafka的连接。
        Returns:
            None
        """
        self.producer_json.close()
        self.producer.close()


if __name__ == '__main__':
    '''脚本调用执行;'''
    kafka_obj = KProducer()
    print(kafka_obj.broker)
    kafka_obj.send(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>自动生成".encode())
