# -*- coding: utf-8 -*-

import json

from polaris_mq.kafka import PolarisKafkaProducer, PolarisKafkaConsumer

def sync_send_test(bootstrap_servers,
                   topic,
                   json_format=True):
    value = {
        "send_type": "sync_send",
        "name": "lady_killer",
        "age": 18
    }
    if json_format:
        p = PolarisKafkaProducer(bootstrap_servers=bootstrap_servers)
        p.sync_send(value,topic)
    else:
        p = PolarisKafkaProducer(bootstrap_servers=bootstrap_servers,key_serializer=None,value_serializer=None)
        v = bytes('{}'.format(json.dumps(value)), 'utf-8')
        p.sync_send(v,topic)
    p.close()

def async_send_test(bootstrap_servers,
                    topic,
                    json_format=True):
    value = {
        "send_type": "async_send",
        "name":"lady_killer",
        "age":18
    }
    if json_format:
        p = PolarisKafkaProducer(bootstrap_servers=bootstrap_servers)
        p.asyn_send(value,topic)
    else:
        p = PolarisKafkaProducer(bootstrap_servers=bootstrap_servers,key_serializer=None,value_serializer=None)
        v = bytes('{}'.format(json.dumps(value)), 'utf-8')
        p.asyn_send(v,topic)
    p.close()

def consumer_test(bootstrap_servers,
                  topic):
    c = PolarisKafkaConsumer(bootstrap_servers=bootstrap_servers,topic=topic,group_id='test',auto_offset_reset="earliest")
    for data in c.get_consumer():
        print(type(data.value),data.value)
        print(json.loads(data.value))

def get_one_msg(bootstrap_servers,
                topic,
                partition,offset):
    c = PolarisKafkaConsumer(bootstrap_servers=bootstrap_servers, topic=topic, group_id='test', auto_offset_reset="earliest")
    msg = c.get_message_by_partition_offset(partition,offset)
    print(msg)


if __name__ == '__main__':
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    bootstrap_servers = ['10.53.0.73:9092','10.53.0.74:9092','10.53.0.75:9092']
    topic = "kw-sync"
    # 测试生产
    # sync_send_test(bootstrap_servers=bootstrap_servers,topic=topic)
    # async_send_test(bootstrap_servers=bootstrap_servers,topic=topic)
    sync_send_test(bootstrap_servers=bootstrap_servers,topic=topic,json_format=False)
    async_send_test(bootstrap_servers=bootstrap_servers,topic=topic,json_format=False)
    # 测试消费
    consumer_test(bootstrap_servers=bootstrap_servers,topic=topic)
    # get_one_msg(bootstrap_servers=bootstrap_servers,topic=topic,partition=0,offset=0)
