# -*- coding: utf-8 -*-

from kafka import KafkaConsumer

consumer = KafkaConsumer('kw-sync', bootstrap_servers=['10.53.0.73:9092','10.53.0.74:9092','10.53.0.75:9092'],group_id='my_favorite_group')

for msg in consumer:
    print (msg)

