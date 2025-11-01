# -*- coding: utf-8 -*-

"""
descr: lunix client
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: lunix_client.py
"""


class LunixClient:

    def __init__(self,
                 host="localhost",
                 port=22,
                 username="username",
                 password="password"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def _get_conn(self,host):
        print(">>>>>>>>>>>>>>")

    def execute_command(self,command):
        print(">>>>>>>>>>>>>>")


