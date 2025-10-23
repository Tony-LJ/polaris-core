# -*- coding: utf-8 -*-

"""
descr: minio client客户端
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: minio_client.py
"""
from polaris_common import CommonUtils
import logging
import minio

class MinioClient:
    """ minio工具类
    conf = {
        'endpoint': '110.110.110.110:9000',
        'access_key': 'admin',
        'secret_key': '123456',
        'secure': False,
    }
    """
    CONN = None
    CFID = None
    POLICY = '{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"AWS":["*"]},"Action":["s3:GetBucketLocation","s3:ListBucket"],"Resource":["arn:aws:s3:::%s"]},{"Effect":"Allow","Principal":{"AWS":["*"]},"Action":["s3:GetObject"],"Resource":["arn:aws:s3:::%s/*"]}]}'

    @classmethod
    def _init(cls, conf: dict):
        """
         init
        :param conf:
        :return:
        """
        if cls.CONN is None:
            cls.connect(conf)
        elif cls.CFID != CommonUtils.get_uuid(conf):
            cls.connect(conf)

    @classmethod
    def connect(cls, conf: dict):
        """
        连接
        :param conf:
        :return:
        """
        try:
            cls.CONN = minio.Minio(**conf)
            cls.CFID = CommonUtils.get_uuid(conf)
        except Exception as e:
            logging.error("minio init failed, please check the config", e)

    @classmethod
    def upload(cls, conf: dict, bucket: str, filepath: str, filename: str):
        """
        上传文件，返回文件的下载地址
        :param conf:
        :param bucket:
        :param filepath:
        :param filename:
        :return:
        """
        cls._init(conf)
        endpoint = conf['endpoint']
        download_url = f'http://{endpoint}'
        cls.CONN.fput_object(bucket_name=bucket, object_name=filename, file_path=filepath)
        return f'{download_url}/{bucket}/{filename}'

    @classmethod
    def exists_bucket(cls, conf: dict, bucket: str):
        """
        判断桶是否存在
        :param bucket_name: 桶名称
        :return:
        """
        cls._init(conf)
        return cls.CONN.bucket_exists(bucket_name=bucket)

    @classmethod
    def create_bucket(cls, conf: dict, bucket: str, is_policy: bool = True):
        """
        创建桶 + 赋予策略
        :param bucket_name: 桶名
        :param is_policy: 策略
        :return:
        """
        cls._init(conf)
        if cls.exists_bucket(bucket=bucket):
            return False
        else:
            cls.CONN.make_bucket(bucket_name=bucket)
        if is_policy:
            policy = cls.POLICY % (bucket, bucket)
            cls.CONN.set_bucket_policy(bucket_name=bucket, policy=policy)
        return True

    @classmethod
    def download(cls, conf: dict, bucket: str, filepath: str, filename: str):
        """
        下载保存文件保存本地
        :param bucket:
        :param filepath:
        :param filename:
        :return:
        """
        cls._init(conf)
        cls.CONN.fget_object(bucket, filename, filepath)