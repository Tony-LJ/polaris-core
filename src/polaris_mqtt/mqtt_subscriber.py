# -*- coding: utf-8 -*-

"""
descr: MQTT订阅消息
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: mqtt_subscriber.py
"""
import paho.mqtt.client as mqtt
import json


class MQTTSubscriber:
    """
    MQTT订阅消息的类
    """
    def __init__(self, host, port=1883, client_id="", username=None, password=None):
        """
        初始化 MQTT 客户端的连接信息
        :param host:
        :param port:
        :param client_id:
        :param username:
        :param password:
        """
        # MQTT 服务器的地址
        self.host = host
        # MQTT 服务器的端口号，默认为 1883
        self.port = port
        # 创建一个 MQTT 客户端对象，传入客户端 ID
        self.client = mqtt.Client(client_id=client_id)

        # 如果提供了用户名和密码，就设置 MQTT 客户端的认证信息
        if username and password:
            self.client.username_pw_set(username, password)

        # 设置自动重连的时间间隔，最小为 1 秒，最大为 120 秒
        self.client.reconnect_delay_set(min_delay=1, max_delay=120)

        # 初始化消息
        self.message = None

    def on_connect(self, client, userdata, flags, rc):
        """连接成功回调函数"""
        # 打印连接结果，0 表示成功，其他值表示失败
        print("connect：", rc)

        # 订阅指定主题的消息，传入主题和消息质量等级
        self.client.subscribe(self.topic, self.qos)

    def on_message(self, client, userdata, msg):
        """订阅消息回调函数，当收到订阅的消息时被调用"""
        try:
            # 将消息中的JSON字符串转换为Python字典对象
            self.message = json.loads(msg.payload.decode('gb2312'))
        except ValueError:
            # 如果无法转换为Python字典对象，则直接使用字符串格式
            self.message = msg.payload.decode('gb2312')

        # 打印收到的消息的主题和内容
        print(f"主题: {msg.topic} 消息: {self.message}")

    def get_message(self):
        """获取最新的消息"""
        return self.message

    def subscribe(self, topic, qos=0):
        """
        连接 MQTT 服务器，并订阅消息
        :param topic:
        :param qos:
        :return:
        """
        # 订阅的主题
        self.topic = topic
        # 消息质量等级
        self.qos = qos
        # 设置连接成功回调函数
        self.client.on_connect = self.on_connect
        # 设置订阅消息回调函数
        self.client.on_message = self.on_message
        # 连接MQTT服务器，keepalive为60秒，表示每隔60秒发送一次心跳包
        self.client.connect(self.host, self.port, keepalive=60)
        # 启动一个新的线程来处理网络交互
        self.client.loop_start()

    def disconnect(self):
        """
        断开 MQTT 服务器连接
        :return:
        """
        # 断开连接
        self.client.disconnect()
        # 停止线程
        self.client.loop_stop()


# if __name__ == "__main__":
#     # 设置MQTT服务器地址，客户端 ID
#     subscriber = MQTTSubscriber("test.mosquitto.org", client_id="my_client_id")
#
#     # 连接MQTT服务器，并订阅消息，传入主题和消息质量等级
#     subscriber.subscribe(topic="topic/test", qos=1)

