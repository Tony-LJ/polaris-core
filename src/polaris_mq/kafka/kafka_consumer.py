# -*- coding: utf-8 -*-
"""
descr: kafka consumer客户端
auther: lj.michale
create_date: 2025/10/27 15:54
file_name: kafka_consumer.py
"""
import json
import traceback
from kafka import KafkaConsumer, KafkaProducer, TopicPartition
from typing import List


class PolarisKafkaConsumer:
    """
    descr: kafka consumer
    """
    def __init__(self, bootstrap_servers: List, topic: str, group_id: str, key_deserializer=None,
                 value_deserializer=None, auto_offset_reset="latest"):
        self.topic = topic
        try:
            self.consumer = KafkaConsumer(
                self.topic,
                bootstrap_servers=bootstrap_servers,
                group_id=group_id,
                enable_auto_commit=False,
                auto_commit_interval_ms=1000,
                session_timeout_ms=30000,
                max_poll_records=50,
                max_poll_interval_ms=30000,
                metadata_max_age_ms=3000,
                key_deserializer=key_deserializer,
                value_deserializer=value_deserializer,
                auto_offset_reset=auto_offset_reset
            )
            self.consumer.subscribe(topics=[self.topic])
            print("connect to kafka and subscribe topic success")
        except Exception as e:
            raise Exception("Kafka pconsumers set connect fail, {0}, {1}".format(e, traceback.print_exc()))

    def get_consumer(self):
        """
        返会可迭代consumer
        :return: consumer
        """
        return self.consumer

    def set_topic(self, topic: str):
        """
        订阅主题
        :param topic: 主题
        :return: None
        """
        self.topic = topic
        self.consumer.subscribe(topics=[self.topic])

    def get_message_by_partition_offset(self, partition, offset):
        """
        通过partition、offset获取一个消息
        :param partition: 分区
        :param offset: 游标、下标、序号
        :return: message，消息
        """
        self.consumer.unsubscribe()
        partition = TopicPartition(self.topic, partition)
        self.consumer.assign([partition])
        self.consumer.seek(partition, offset=offset)
        for message in self.consumer:
            return message