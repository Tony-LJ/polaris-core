# -*- coding: utf-8 -*-
"""
descr: kafka producer客户端
auther: lj.michale
create_date: 2025/10/27 15:54
file_name: kafka_producer.py
"""
import json
import traceback
from kafka import KafkaConsumer, KafkaProducer, TopicPartition
from typing import List


class PolarisKafkaProducer:
    """
    descr: kafka producer
    """
    def __init__(self,
                 bootstrap_servers: List,
                 key_serializer=lambda m: json.dumps(m).encode("ascii"),
                 value_serializer=lambda m: json.dumps(m).encode("ascii"), compression_type=None):
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=bootstrap_servers,
                buffer_memory=33554432,
                batch_size=1048576,
                max_request_size=1048576,
                key_serializer=key_serializer,
                value_serializer=value_serializer,
                compression_type=compression_type  # 压缩消息发送 gzip lz4 snappy zstd
            )
            print("connect success, kafka producer info {0}".format(bootstrap_servers))
        except Exception as e:
            raise Exception("connect kafka failed, {}.".format(e))

    def sync_send(self, topic: str, data):
        """
        同步发送数据
        :param data:  发送数据
        :param topic: 主题
        :return: partition, offset
        """
        try:
            future = self.producer.send(topic, data)
            record_metadata = future.get(timeout=10)  # 同步确认消费
            partition = record_metadata.partition  # 数据所在的分区
            offset = record_metadata.offset  # 数据所在分区的位置
            print("save success, partition: {}, offset: {}".format(partition, offset))
            return partition, offset
        except Exception as e:
            raise Exception("Kafka sync send failed, {}.".format(e))

    def async_send(self, topic: str, data):
        """
        异步发送数据
        :param data:  发送数据
        :param topic: 主题
        :return: None
        """
        try:
            self.producer.send(topic, data)
            print("send data:{}".format(data))
        except Exception as e:
            raise Exception("Kafka asyn send failed, {}.".format(e))

    def async_callback(self, topic: str, data):
        """
        异步发送数据 + 发送状态处理
        :param data:发送数据
        :param topic: 主题
        :return: None
        """
        try:
            for item in data:
                self.producer.send(topic, item).add_callback(self.__send_success).add_errback(self.__send_error)
                self.producer.flush()  # 批量提交
        except Exception as e:
            raise Exception("Kafka asyn send fail, {}.".format(e))

    @staticmethod
    def __send_success():
        """异步发送成功回调函数"""
        print("save success")
        return

    @staticmethod
    def __send_error():
        """异步发送错误回调函数"""
        print("save error")
        return

    def close(self):
        self.producer.close()
