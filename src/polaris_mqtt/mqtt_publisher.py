# -*- coding: utf-8 -*-

"""
descr: MQTT消息发布
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: mqtt_publisher.py
"""
import paho.mqtt.client as mqtt
import json

class MQTTPublisher:
    """
    MQTT发布消息的类
    """
    def __init__(self,
                 host,
                 port=1883,
                 client_id="", username=None, password=None):
        """
        构造函数，用于初始化 MQTT 客户端的连接信息
        :param host: str，MQTT 服务器地址
        :param port: int，MQTT 服务器端口，默认为1883
        :param client_id: str，MQTT 客户端 ID，默认为空
        :param username: str，MQTT 服务器用户名（可选）
        :param password: str，MQTT 服务器密码（可选）
        """
        self.host = host
        self.port = port
        self.client = mqtt.Client(client_id=client_id)

        # 如果提供了用户名和密码，就设置 MQTT 客户端的认证信息
        if username and password:
            self.client.username_pw_set(username, password)

    def on_connect(self, client, userdata, flags, rc):
        """
        连接成功回调函数，会在 MQTT 客户端连接成功时被调用

        :param client: MQTT 客户端实例
        :param userdata: 用户数据
        :param flags: 标志位
        :param rc: 返回码

        - 返回码说明：
            * 0：连接成功
            * 1：协议版本不正确
            * 2：客户端标识符无效
            * 3：服务器不可用
            * 4：用户名或密码不正确
            * 5：未经授权
        """
        rc_status = [
            "连接成功", "协议版本不正确", "客户端标识符无效", "服务器不可用", "用户名或密码不正确", "未经授权"]
        print("connect：", rc_status[rc], rc)

    def connect(self):
        """
        连接 MQTT 服务器
        """
        # 设置连接成功回调函数
        self.client.on_connect = self.on_connect

        # 连接MQTT服务器，keepalive为60秒
        self.client.connect(self.host, self.port, keepalive=60)

        # 启动一个单独的线程来处理网络流量和消息接收
        self.client.loop_start()

    def disconnect(self):
        """
        断开 MQTT 服务器连接
        """
        self.client.disconnect()

    def publish(self, topic, message, qos=0):
        """
        发布 MQTT 消息到指定主题
        :param topic: MQTT 消息主题
        :param message: MQTT 消息内容，需要将其转换成JSON字符串
        :param qos: MQTT 消息质量等级，默认为0
        - qos说明：
            * 0：最多一次，不保证消息能够被接收到
            * 1：至少一次，确保消息至少被接收到一次，可能会重复发送
            * 2：恰好一次，确保消息只被接收到一次，但可能会增加网络负载
        """
        # 连接 MQTT 服务器
        self.connect()

        # 将消息内容转换成JSON字符串，然后使用'gb2312'编码
        message_str = json.dumps(message, ensure_ascii=False).encode('gb2312')

        # 发布MQTT消息到指定主题，并指定质量等级
        self.client.publish(topic, message_str, qos=qos)

        # 停止循环处理网络流量和消息接收
        self.client.loop_stop()


# if __name__ == "__main__":
#     # 设置MQTT服务器地址，客户端 ID
#     publisher = MQTTPublisher("test.mosquitto.org", client_id="my_client_id")
#
#     # 发布MQTT消息到指定主题（项目中mqtt协议如果有固定部分，建议封装到publish方法中，传入data即可）, 质量等级为1
#     message = {
#         "user": "admin",
#         "password": 123
#     }
#     publisher.publish("topic/test", message, 1)
#
#     # 主线程结束，子线程会自动断开MQTT连接，如主线程一直运行，需要关闭mqtt连接时，调用disconnect()方法断开连接
#     publisher.disconnect()


