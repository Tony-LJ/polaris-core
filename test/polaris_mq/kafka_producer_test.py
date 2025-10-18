# -*- coding: utf-8 -*-

import json
from kafka import KafkaProducer

from polaris_mq.kafka import PolarisKafkaProducer


def sync_send_test(bootstrap_servers,topic,json_format=True):
    value = '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>send_type'
    if json_format:
        p = PolarisKafkaProducer(bootstrap_servers=bootstrap_servers)
        p.sync_send(value,topic)
    else:
        p = PolarisKafkaProducer(bootstrap_servers=bootstrap_servers,key_serializer=None,value_serializer=None)
        v = bytes('{}'.format(json.dumps(value)), 'utf-8')
        p.sync_send(v,topic)
    p.close()

if __name__ == '__main__':
    bootstrap_servers=['10.53.0.73:9092','10.53.0.74:9092','10.53.0.75:9092']
    topic = "kw-sync"
    sync_send_test(bootstrap_servers=bootstrap_servers,topic=topic)


# producer = KafkaProducer(bootstrap_servers=['10.53.0.73:9092','10.53.0.74:9092','10.53.0.75:9092'])
#
# for i in range(1000):
#     message = json.dumps({'name': 'kafka', 'index': i}).encode('utf-8')
#     producer.send('kw-sync', message)
#     print(message.decode('utf-8'))
#
# producer.flush()

