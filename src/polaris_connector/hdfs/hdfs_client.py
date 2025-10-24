# -*- coding: utf-8 -*-

"""
descr: hdfs客户端封装
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: hdfs_client.py
"""
from hdfs import InsecureClient

class HdfsClient:
    def __init__(self, host='default'):
        """
        初始化HDFS客户端。
        :param host: HDFS服务器地址，默认为'default'。
        """
        self.client = InsecureClient(host, user="hdfs")  # 使用InsecureClient进行非Kerberos认证连接。对于Kerberos认证，请使用KerberosClient。

    def list_files(self, hdfs_path):
        """
        列出文件
        :param hdfs_path:
        :return:
        """
        files = self.client.list(hdfs_path)
        print(f"Files in {hdfs_path}: {files}")
        return files

    def list_directory(self, path):
        """
        列出HDFS目录下的文件和目录
        :param path:
        :return:
        """
        return self.client.list(path)['files']

    def read_file(self, path):
        """
        读取HDFS文件内容
        :param path:
        :return:
        """
        with self.client.read(path, encoding='utf-8') as reader:
            return reader.read()

    def list_files_and_dirs(self, hdfs_path):
        """
        列出指定HDFS路径下的文件和目录
        :param hdfs_path:
        :return:
        """
        print(f"\n列出路径 {hdfs_path} 下的内容:")
        try:
            contents = self.list(hdfs_path)
            for item in contents:
                print(f"- {item}")
            return contents
        except Exception as e:
            print(f"列出内容失败: {e}")
            return []

    # def write_file(self, path, data):
    #     """写入数据到HDFS文件"""
    #     with self.client.write(path, encoding='utf-8') as writer:


if __name__ == '__main__':
    client = HdfsClient("http://10.53.0.71:9870",)
    print(client.list_files("/user/hive/warehouse/bi_ads.db"))
    # print("hdfs中的目录为:", client.list(hdfs_path="/",status=True))

