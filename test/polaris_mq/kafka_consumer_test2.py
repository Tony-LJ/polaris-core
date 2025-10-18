# -*- coding: utf-8 -*-

import json

from kafka import KafkaConsumer, KafkaProducer
from kafka.structs import TopicPartition


class KConsumer(object):
    """kafka 消费者; 动态传参,非配置文件传入;
       kafka 的消费者应该尽量和生产者保持在不同的节点上;否则容易将程序陷入死循环中;
    """

    _encode = "UTF-8"

    def __init__(self, topics="start_server", bootstrap_server=None, group_id="start_task", partitions=None, **kwargs):
        """ 初始化kafka的消费者;
            1. 设置默认 kafka 的主题, 节点地址, 消费者组 id(不传入的时候使用默认的值)
            2. 当需要设置特定参数的时候可以直接在 kwargs 直接传入,进行解包传入原始函数;
            3. 手动设置偏移量
        Args:
            topics: str; kafka 的消费主题;
            bootstrap_server: list; kafka 的消费者地址;
            group_id: str; kafka 的消费者分组 id,默认是 start_task 主要是接收并启动任务的消费者,仅此一个消费者组id;
            partitions: int; 消费的分区,当不使用分区的时候默认读取是所有分区;
            **kwargs: dict; 其他原生kafka消费者参数的;
        """

        if bootstrap_server is None:
            bootstrap_server = ['10.53.0.73:9092','10.53.0.74:9092','10.53.0.75:9092']  # kafka集群的话就写多个
        self.consumer = KafkaConsumer(bootstrap_servers=bootstrap_server)
        exist = self.exist_topics(topics)
        if not exist:  # 需要的主题不存在;
            # 创建一条
            self.create_topics(topics)
        if partitions is not None:
            self.consumer = KafkaConsumer(
                bootstrap_servers=bootstrap_server,
                group_id=group_id,
                # 目前只有一个消费者,根据情况是否需要进行修改;当扩展多个消费者的时候需要进行扩展;
                **kwargs
            )
            # print("指定分区信息:", partitions, topics, type(partitions))
            self.topic_set = TopicPartition(topics, int(partitions))
            self.consumer.assign([self.topic_set])
        else:
            # 默认读取主题下的所有分区, 但是该操作不支持自定义 offset, 因为 offset 一定是在指定的分区中进行的;
            self.consumer = KafkaConsumer(
                topics,
                bootstrap_servers=bootstrap_server,
                group_id=group_id,
                **kwargs
            )

    def exist_topics(self, topics):
        """
        检查 kafka 中的主题是否存在;
        Args:
            topics: 主题名称;

        Returns:
            bool: True/False ; True,表示存在,False 表示不存在;
        """
        topics_set = set(self.consumer.topics())
        if topics not in topics_set:
            return False
        return True

    @staticmethod
    def create_topics(topics):
        """
        创建相关的 kafka 主题信息;说明本方法可以实现用户自定义 kafka 的启动服务,默认是使用的是 start_server;
        Args:
            topics: str; 主题的名字;

        Returns:
            None
        """
        producer = KafkaProducer(
            bootstrap_servers='192.168.74.136:9092',
            key_serializer=lambda k: json.dumps(k).encode('utf-8'),
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )
        producer.send(topics, key="start", value={"msg": "aaaa"})
        producer.close()

    def recv(self):
        """
        接收消费中的数据
        Returns:
            使用生成器进行返回;
        """
        for message in self.consumer:
            # 这是一个永久阻塞的过程,生产者消息会缓存在消息队列中,并且不删除,所以每个消息在消息队列中都会有偏移
            # print("主题:%s 分区:%d:连续值:%d: 键:key=%s 值:value=%s" % (
            #     message.topic, message.partition, message.offset, message.key, message.value))
            yield {"topic": message.topic, "partition": message.partition, "key": message.key,
                   "value": message.value.decode(self._encode)}

    def recv_seek(self, offset):
        """
        接收消费者中的数据,按照 offset 的指定消费位置;
        Args:
            offset: int; kafka 消费者中指定的消费位置;

        Returns:
            generator; 消费者消息的生成器;
        """
        self.consumer.seek(self.topic_set, offset)
        for message in self.consumer:
            # print("主题:%s 分区:%d:连续值:%d: 键:key=%s 值:value=%s" % (
            #     message.topic, message.partition, message.offset, message.key, message.value))
            yield {"topic": message.topic,
                   "partition": message.partition,
                   "key": message.key,
                   "value": message.value.decode(self._encode)}


if __name__ == '__main__':
    """ 
    测试使用
    """
    obj = KConsumer("kw-sync", bootstrap_server=['10.53.0.73:9092','10.53.0.74:9092','10.53.0.75:9092'])
    for i in obj.recv():
        print(i)

