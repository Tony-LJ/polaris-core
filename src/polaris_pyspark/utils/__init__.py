# -*- coding: utf-8 -*-
import logging
import os
import re
# import subprocess
import uuid
from contextlib import contextmanager
from datetime import datetime, timedelta
from functools import wraps, reduce
from time import sleep

import pandas as pd
import requests
from numpy import nan
from pandas import DataFrame
import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import expr
from pyspark.sql.readwriter import DataFrameWriter
from pyspark.sql.types import StringType

from ..templates import (get_decrypt_table_name,
                         get_hour_to_day_et_sql,
                         get_insert_partition_table_sql, get_decrypt_data_table_insertion_sql)


# for ETL spark createOrReplaceTempView
raw_data_tmp_view_name = "raw_data__"
corrupt_data_tmp_view_name = "corrupt_raw_data__"
output_tmp_view_name = "hour_data__"
output_tmp_md5_view_name = "hour_data_md5__"

def init_spark(app_name, yarn_queue):
    """
    初始化spark环境
    :param app_name:
    :param yarn_queue:
    :return:
    """
    current_path = os.path.abspath(__file__)
    father_path = os.path.abspath(os.path.join(os.path.dirname(current_path), ".."))
    base_path = father_path + '/jars/'
    jars = os.listdir(base_path)
    jars_path = ','.join(base_path + jar for jar in jars)
    # print(jars_path)
    spark = SparkSession.builder \
        .appName(app_name) \
        .config("spark.yarn.queue", yarn_queue) \
        .config("spark.scheduler.mode", "FAIR") \
        .config("hive.default.fileformat", "parquetfile") \
        .config("spark.jars", jars_path) \
        .enableHiveSupport() \
        .getOrCreate()

    # py4j black magic
    sc = spark.sparkContext
    hadoop = sc._gateway.jvm.org.apache.hadoop
    conf = hadoop.conf.Configuration()
    hdfs = hadoop.fs.FileSystem.get(conf)

    # add hadoop & hdfs to spark
    spark.hadoop = hadoop
    spark.hdfs = hdfs
    spark.registerJavaFunction = spark.udf.registerJavaFunction
    # 给DataFrameWriter的实例添加insertIntoPartition方法
    DataFrameWriter.insertIntoPartition = insert_into_partition
    return spark


@contextmanager
def cache(rdd_or_df):
    """
    context中保证rdd_or_df是cached, 出了context恢复rdd_or_df的cache状态
    :param rdd_or_df: spark rdd or DataFrame
    :return: spark rdd or DataFrame
    """
    is_cached = rdd_or_df.is_cached
    rdd_or_df.cache()
    yield rdd_or_df
    if not is_cached:
        rdd_or_df.unpersist()

def dfs_ls(path, spark=None, sort_by_mtime=True):
    """
    just like `hdfs dfs -ls ${path}`
    :param path: string, can be glob path pattern
    :param spark: None or SparkSession, if None, use shell command `hdfs dfs -ls <path>`
    :param sort_by_mtime: Boolean
    :return: pandas DataFrame, ascending order by time
    """
    output_cols = ["perm", "rep", "owner", "group", "size", "mtime", "path"]

    if not spark:
        pathes = ""
        # pathes = subprocess.check_output("hdfs dfs -ls {}".format(path).split()).strip().split('\n')
        if len(pathes) > 0 and pathes[0].startswith("Found"):  # 首行为类似"Found 90646 items"时直接丢掉
            pathes.pop(0)
        pathes_df = pd.DataFrame(map(str.split, pathes),
                                 columns=["perm", "rep", "owner", "group", "size", "date", "time", "path"])
        pathes_df["mtime"] = pd.to_datetime(pathes_df.date + " " + pathes_df.time)
    else:
        # name_server = spark.hdfs.getName()
        path_status = [
            {
                "path": x.getPath().toString(),
                "rep": x.getReplication(),
                "mtime": x.getModificationTime(),
                "atime": x.getAccessTime(),
                "size": x.getBlockSize(),
                "owner": x.getOwner(),
                "group": x.getGroup(),
                "perm": x.getPermission().toString(),
                "link": x.isSymlink()
            } for x in spark.hdfs.globStatus(spark.hadoop.fs.Path(path))
            # } for x in spark.hdfs.listStatus(spark.hadoop.fs.Path(path))
        ]
        pathes_df = pd.DataFrame(path_status, columns=output_cols)
    if sort_by_mtime:
        pathes_df.sort_values(by="mtime", inplace=True)
    return pathes_df


def dfs_du_s(path, spark):
    """
    just like 'hdfs dfs -du -s ${path}'
    >>> dfs_du_s("/user/hive/warehouse/edw.db/user_location_log/data_date=20191111/abroad=0", spark)
    >>> 1116020512585
    :param path: string
    :param spark: SparkSession
    :return: Long, Size of HDFS directory/file in bytes, without pay attention to replication factor
    """
    return spark.hdfs.getContentSummary(spark.hadoop.fs.Path(path)).getLength()


def dfs_du_s_glob(path, spark):
    """
    just like 'hdfs dfs -du -s ${path}', but path can be a glob pattern
    >>> dfs_du_s_glob("/user/hive/warehouse/edw.db/register_user_latest_hour_log/data_hour=20191111*", spark)
    >>> 2651431904
    :param path: string, can be glob pattern
    :param spark: SparkSession
    :return: long/int, Size of HDFS directory/file in bytes, without pay attention to replication factor
    """
    return sum([dfs_du_s(p, spark) for p in dfs_ls(path, spark).path])


def get_size_before_merge_etl(spark, from_table, partition_col, merged_data_time):
    """
    merge之前from_table所有分区的总大小
    >>> get_size_before_merge_etl(
    >>>     spark, from_table="edw.register_user_latest_hour_log",
    >>>     partition_col="data_hour", merged_data_time="20191111"
    >>> )
    >>> 2651431904
    :param spark: SparkSession
    :param from_table: string
    :param partition_col: string
    :param merged_data_time: string, prefix of data_time
    :return: long/int, total size in bytes
    """
    path_glob = "{table_path}/{partition_col}={merged_data_time}*".format(
        table_path=get_table_location(spark, from_table),
        partition_col=partition_col, merged_data_time=merged_data_time
    )
    return dfs_du_s_glob(path_glob, spark)


def get_hive_table_info(spark, table_name, partition_spec=None):
    """取hive表信息
    :type spark: SparkSession
    :type table_name: string
    :type partition_spec: None or string
    :rtype: (DataFrame, DataFrame, dict, dict)
    """
    # pyspark catalog接口太简陋， 好多信息拿不到
    desc_stmt = "DESC FORMATTED {table}".format(table=table_name) if not partition_spec \
        else "DESC FORMATTED {table} PARTITION ({par_spec})".format(table=table_name, par_spec=partition_spec)
    desc_raw_df = spark.sql(desc_stmt).toPandas()  # type: pd.DataFrame

    desc_raw_df.replace(to_replace='', value=nan, inplace=True)
    desc_raw_df.dropna(axis='index', how='all', inplace=True)
    # spark 2.3 特殊情况
    desc_filtered_df = desc_raw_df.loc[
        desc_raw_df.col_name.str.startswith("#") | desc_raw_df.col_name.str.startswith("Serde Library"),
        "col_name"
    ]  # type: pd.DataFrame
    sep_to_idx = {desc: i for i, desc in desc_filtered_df.iteritems()}
    partition_info_i = sep_to_idx.get('# Partition Information')
    _col_name_i = sep_to_idx.get('# col_name')
    detail_info_i = sep_to_idx['# Detailed Table Information'] if not partition_spec \
        else sep_to_idx['# Detailed Partition Information']
    # spark 2.3 没有# Storage Information 这一行，  为了更改少， Serde Library 这一行将会被忽略
    storage_info_i = sep_to_idx['# Storage Information'] if '# Storage Information' in sep_to_idx \
        else sep_to_idx.get('Serde Library')

    column_info = desc_raw_df.loc[:(partition_info_i if partition_info_i else detail_info_i) - 1]
    if partition_info_i:
        partition_col_info = desc_raw_df.loc[_col_name_i + 1: detail_info_i - 1, ]
    else:
        partition_col_info = pd.DataFrame([], columns=desc_raw_df.columns)
    detail_info = desc_raw_df.loc[detail_info_i + 1: storage_info_i - 1].drop("comment", axis="columns")
    detail_info.rename(columns={"col_name": "key", "data_type": "value"}, inplace=True)
    detail_info.set_index("key", inplace=True)
    storage_info = desc_raw_df.loc[storage_info_i + 1:].drop("comment", axis="columns")
    storage_info.rename(columns={"col_name": "key", "data_type": "value"}, inplace=True)
    storage_info.set_index("key", inplace=True)

    def info_to_dict(info):
        return {k.lower().strip("\t :").replace(' ', '_'): v for k, v in info.itertuples()}

    return column_info, partition_col_info, info_to_dict(detail_info), info_to_dict(storage_info)


def get_table_location(spark, table_name, partition_spec=""):
    """取hive表位置信息
    >>> get_table_location(spark, "edw.user_location_log", partition_spec="data_date=20191111, abroad=0")
    >>> u'hdfs://nfjd-prod-ns2/user/hive/warehouse/edw.db/user_location_log/data_date=20191111/abroad=0'
    >>> get_table_location(spark, "edw.user_location_log")
    >>> u'hdfs://nfjd-prod-ns2/user/hive/warehouse/edw.db/user_location_log'
    :type spark: SparkSession
    :type table_name: string
    :type partition_spec: string, optional. if specified, return partition location, return table location otherwise
    :rtype: string
    """
    _, _, detail_info, _ = get_hive_table_info(spark, table_name, partition_spec)
    return detail_info["location"]


def drop_table_partitions(spark, table_name, partition_specs):
    _, _, table_detail_info, _ = get_hive_table_info(spark, table_name)
    # table_path, table_type = table_detail_info["location"], table_detail_info['table_type']
    table_path = table_detail_info["location"]
    table_type = table_detail_info['table_type'] if table_detail_info.get('table_type') \
        else table_detail_info['type']

    for par_spec in partition_specs:
        logging.warn("drop {table_name} partition {partition_spec}".format(
            table_name=table_name, partition_spec=par_spec))
        drop_partition_stmt = "ALTER TABLE {table_name} DROP IF EXISTS PARTITION ({partition_spec})".format(
            table_name=table_name, partition_spec=par_spec)
        spark.sql(drop_partition_stmt)
        if table_type == "EXTERNAL":
            partition_path = os.path.join(table_path, par_spec)
            spark.hdfs.delete(spark.hadoop.fs.Path(partition_path), True)


# def send_alert(tag, alert, code=276):
#     """ wrap alert message with time and header, then send it to iPortal
#         @alert :: string
#     """
#     if not code:
#         logging.warn("No alert code, skip alert")
#     else:
#         if type(tag) != unicode:
#             tag = tag.decode('utf-8')
#         if type(alert) != unicode:
#             alert = alert.decode('utf-8')
#         requests.post('http://alert.jpushoa.com/v1/alert/',
#                       json={
#                           "code": code,  # 按需自己改, 发送给相应的组
#                           "desc": u" ".join([tag, u"\n", alert])
#                       })


def get_valid_paths(spark, read_base_path, data_time):
    """处理hdfs路径, 多个read_base_path用','分割, 归档(.har)会加上前缀(har://)后缀(.har)
    :param spark: SparkSession
    :param read_base_path: ','分割路径字符串, 可包含多个路径
    :param data_time: string,
    :return: [string], list of valid_paths
    """
    valid_paths = []
    paths = read_base_path.split(",")
    for path in paths:
        read_path = os.path.join(path, data_time)
        if spark.hdfs.exists(spark.hadoop.fs.Path(read_path)):
            valid_paths.append(read_path)
        elif spark.hdfs.exists(spark.hadoop.fs.Path(read_path + '.har')):
            valid_paths.append('har://' + read_path + '.har')
        else:
            logging.warn("Path does not exist: " + read_path + '(.har)')
    return valid_paths


def get_rdds(spark, read_base_path, data_time):
    """读取hdfs上textFile为rdd. 直接读取成DataFrame无法正确处理har文件, schema中nullable属性也不生效
    并且有control char的json会被整行当成corrupt_record, 不符合预期. 所以这里统一先读成rdd再处理
    :type spark: SparkSession
    :type read_base_path: string
    :type data_time: string
    :rtype: [rdd]
    """
    sc = spark.sparkContext
    valid_paths = get_valid_paths(spark, read_base_path, data_time)
    if not valid_paths:
        return []
    else:
        rdds = [sc.textFile(valid_path) for valid_path in valid_paths]
    return rdds


def rdds_to_df(spark, rdds, file_type, read_data_schema, column_name_of_corrupt_record, use_cache=True, read_args=None):
    """
    :param use_cache:
    :param spark: SparkSession
    :param rdds: [rdd], result of function `get_rdds`
    :param file_type: str, "json" or "csv"
    :param read_data_schema: StructType
    :param column_name_of_corrupt_record: string, (columnNameOfCorruptRecord)
    :param read_args: other args for spark.read.csv or spark.read.json
    :return: DataFrame
    """
    read_args = {} if not read_args else read_args  # read_args default: {}
    if file_type == 'json':
        dfs = [spark.read.json(
            path=rdd, schema=read_data_schema,
            mode='PERMISSIVE', columnNameOfCorruptRecord=column_name_of_corrupt_record, **read_args
        ) for rdd in rdds]
    elif file_type == 'csv':
        dfs = [spark.read.csv(
            path=rdd, schema=read_data_schema,
            mode='PERMISSIVE', columnNameOfCorruptRecord=column_name_of_corrupt_record, **read_args
        ) for rdd in rdds]
    else:
        dfs = []
        logging.error("read file type error!")
        exit(1)
    if use_cache:  # 正常数据和corrupted records分别处理, 多次读取解析json文件. cache减少重复解析json/IO
        for df in dfs:
            df.cache()
    raw_data = reduce(lambda l, r: l.union(r), dfs)
    return raw_data


def periodic_etl(spark, read_base_path, read_data_schema,
                 data_table, data_time, transform,
                 column_name_of_corrupt_record, data_corrupt_record_table,
                 debug=False, md5_columns=(), partition_col='data_hour',
                 file_type='json', read_args=None,
                 skip_empty_read_path=True, use_cache=True,
                 enable_hbo=False, min_output_file_size=0):
    """
    Extract from {read_base_path}/{hour} with {read_data_schema}
    Transform
    Load overwrite into {hour_table} partition (data_hour={hour})
    :param spark: SparkSession
    :param read_base_path: string, path of raw json file
    :param read_data_schema: StructType
    :param data_table: string, output hive table name
    :param data_time: string, yyyyMMddHH,yyyyMMdd,yyyyMM
    :param transform: DataFrame -> DataFrame
    :param column_name_of_corrupt_record: string, (columnNameOfCorruptRecord)
    :param data_corrupt_record_table: string, hive table name
    :param debug: bool, debug flag. if True, then will not clean temp views and caches
    :param md5_columns: list of str
    :param partition_col:  str
    :param file_type: str, "json" or "csv"
    :param read_args: other args for spark.read.csv or spark.read.json
    :param skip_empty_read_path: bool, if False, raise Exception when not data in read path
    :param use_cache: read/parse json only once
    :param enable_hbo: bool, enable history based optimization flag
    :param min_output_file_size: int, default 0. try reduce file number by this value if not 0
    :return: int, count of corrupted records in raw_data
    """
    read_args = {} if not read_args else read_args  # read_args default: {}
    rdds = get_rdds(spark, read_base_path, data_time)
    if not rdds:
        if skip_empty_read_path:
            return 0  # return corrupt_cnt = 0
        else:
            raise Exception("empty read path")

    raw_data = rdds_to_df(spark, rdds, file_type, read_data_schema, column_name_of_corrupt_record,
                          use_cache=use_cache, read_args=read_args)
    raw_data.createOrReplaceTempView(raw_data_tmp_view_name)

    # corrupted records
    corrupt_record_df = raw_data.where(
        "{corrupt_col} IS NOT NULL".format(corrupt_col=column_name_of_corrupt_record)
    ).select(column_name_of_corrupt_record).cache()
    corrupt_cnt = corrupt_record_df.count()
    if corrupt_cnt > 0:
        corrupt_record_df.createOrReplaceTempView(corrupt_data_tmp_view_name)
        spark.sql("""INSERT OVERWRITE TABLE {data_table} PARTITION ({partition_col}={data_time})
         SELECT {corrupt_col} AS corrupt_record FROM {tmp_view_name}""".format(
            data_table=data_corrupt_record_table, data_time=data_time, tmp_view_name=corrupt_data_tmp_view_name,
            corrupt_col=column_name_of_corrupt_record, partition_col=partition_col
        ))

    raw_data_without_corrupt = raw_data.where(
        "{corrupt_col} IS NULL".format(corrupt_col=column_name_of_corrupt_record)
    ).drop(column_name_of_corrupt_record)
    data = transform(raw_data_without_corrupt)

    data.createOrReplaceTempView(output_tmp_view_name)

    # 加密分别落对照表
    if md5_columns:
        data.cache()
        decrypt_hour_table_insertion_sql = get_decrypt_data_table_insertion_sql(
            data_table=get_decrypt_table_name(data_table), source_table=output_tmp_view_name,
            md5_columns=md5_columns, data_time=data_time, partition_col=partition_col
        )
        spark.sql(decrypt_hour_table_insertion_sql)
        data_md5 = data.selectExpr(*[
            "md5({col}) AS {col}".format(col=col) if col in md5_columns else col for col in data.columns
        ])
        data_md5.createOrReplaceTempView(output_tmp_md5_view_name)

    # 正常数据落地
    materialize_df = data if not md5_columns else data_md5

    # 基于输入数据量调整materialize_df的partition数量, 即写hdfs的输出表文件数量
    if enable_hbo and min_output_file_size != 0:
        try:
            last_par = get_last_partition(spark, data_table)  # raise exception if empty
            last_data_time = last_par.split("=")[1]
            expansion_rate = estimate_expansion_rate(spark, read_base_path, last_data_time, data_table, partition_col)
            file_num = estimate_output_partition_num(spark, read_base_path, data_time, expansion_rate, min_output_file_size)
            partition_num_before = materialize_df.rdd.getNumPartitions()
            file_num = min(partition_num_before, file_num)
            logging.warn(
                "reduce file num of {output_table} partition {data_time} from {num_before} to {num_after}".format(
                    output_table=data_table, data_time=data_time, num_before=partition_num_before, num_after=file_num
                )
            )
            materialize_df = materialize_df.coalesce(file_num)
        except Exception as ex:
            if type(ex) is AssertionError and ex.message.startswith("empty table"):  # no history, no history based optimization
                logging.warn("empty table, no history yet, no HBO is available. skip HBO")
            else:  # log and skip HBO reduce output file num
                logging.exception("periodic_etl HBO reduce output file num by min_output_file_size failed, skip HBO")

    materialize_df.write.insertIntoPartition(
        tableName=data_table, partitionCol=partition_col, partition=data_time, overwrite=True
    )

    # clean up
    if not debug:
        raw_data.unpersist()
        data.unpersist()
        corrupt_record_df.unpersist()
        spark.catalog.dropTempView(raw_data_tmp_view_name)
        spark.catalog.dropTempView(corrupt_data_tmp_view_name)
        spark.catalog.dropTempView(output_tmp_view_name)
        spark.catalog.dropTempView(output_tmp_md5_view_name)

    return corrupt_cnt


# TODO rename to merge_etl?
def hour_to_day_etl(spark, hour_table, day_table, data_date, distinct_row=False, transform_day=None,
                    enable_hbo=False, min_output_file_size=0):
    """
    :param spark: SparkSession
    :param hour_table: string
    :param day_table: string
    :param data_date: string, merged partition value
    :param distinct_row: string, distinct by row flag
    :param transform_day: DataFrame -> DataFrame
    :param enable_hbo: bool, enable history based optimization flag
    :param min_output_file_size: int, default 0. try reduce file number by this value if not 0
    :return: None
    """
    # spark-sql OVERWRITE external table 真会把之前的数据清除掉, hive不会
    # TODO maybe just copy hdfs file? """
    cols = spark.table(hour_table).columns
    hour_to_day_et_sql = get_hour_to_day_et_sql(
        from_table=hour_table, cols=cols, data_date=data_date, distinct_row=distinct_row, old_partition_col="data_hour"
    )
    day_table_par_df = spark.sql(hour_to_day_et_sql)  # type: pyspark.sql.DataFrame
    # 判断小时表数据是否为null
    if len(day_table_par_df.take(1)) == 0:
        logging.warn("hour data is null, please check hour log!")
        return
    if transform_day is not None:
        day_table_par_df = transform_day(day_table_par_df)

    # 基于输入数据量调整day_table_par_df的partition数量, 即写hdfs的输出表文件数量
    if min_output_file_size != 0:
        input_total_size = get_size_before_merge_etl(
            spark, from_table=hour_table, partition_col="data_hour", merged_data_time=data_date
        )
        partition_num_before = day_table_par_df.rdd.getNumPartitions()
        file_num = partition_num_before  # default: keep partition num
        if not distinct_row and not transform_day:  # 简单合并, 可以直接从输入表估计合适文件数量
            file_num = max(1, int(input_total_size / min_output_file_size))
        elif enable_hbo:  # 有额外处理, HBO估算合适输出文件数量
            try:
                last_par = get_last_partition(spark, day_table)  # raise exception if empty
                last_day_time = last_par.split("=")[1]
                last_input_total_size = get_size_before_merge_etl(
                    spark, from_table=hour_table, partition_col="data_hour", merged_data_time=last_day_time
                )
                last_output_path = get_table_location(
                    spark, table_name=day_table, partition_spec="data_date="+last_day_time)
                last_output_size = dfs_du_s(last_output_path, spark)
                expansion_rate = float(last_output_size) / last_input_total_size
                file_num = max(1, int(input_total_size * expansion_rate / min_output_file_size))
            except Exception as ex:
                if type(ex) is AssertionError and ex.message.startswith("empty table"):  # no history, no history based optimization
                    logging.warn("empty table, no history yet, no HBO is available. skip HBO")
                else:  # log and skip HBO reduce output file num
                    logging.exception("hour_to_day_etl HBO reduce output file num by min_output_file_size failed, skip HBO")

        file_num = min(partition_num_before, file_num)
        logging.warn(
            "reduce file num of {output_table} partition {data_time} from {num_before} to {num_after}".format(
                output_table=day_table, data_time=data_date, num_before=partition_num_before, num_after=file_num
            )
        )
        day_table_par_df = day_table_par_df.coalesce(file_num)

    day_table_par_df.write.insertIntoPartition(
        tableName=day_table, partitionCol="data_date", partition=data_date, overwrite=True
    )


def get_partition(spark, table_name, sort=True, partition_col=None, sep=' and '):
    """ 读取分区，可指定分区名
    :param spark: SparkSession
    :param table_name: hive table name
    :param sort:  (default:True)
    :param partition_col: hive partition name (default:None)
    :param sep: delimiter string for multiple partition columns in return value
    :return: dataframe
    """
    partition_df = spark.sql("show partitions {table}".format(table=table_name)).toPandas()
    partition_df.partition = partition_df.partition.str.replace(pat=u'/', repl=sep)
    if partition_col:
        split_par_df = DataFrame(
            {p.split('=')[0].strip(): p for p in row.split(sep)} for row in partition_df.partition
        )
        if partition_col in split_par_df:
            partition_df = split_par_df[partition_col].to_frame("partition")
            partition_df.drop_duplicates(inplace=True)
        else:
            raise Exception("{col} is not a partition column of table {tb}".format(col=partition_col, tb=table_name))
    if sort:
        partition_df.sort_values(by="partition", ascending=True, inplace=True)
    return partition_df


def get_last_partition(spark, table_name):
    partitions = get_partition(spark, table_name)
    assert len(partitions) >= 1, "empty table: " + table_name
    last_partition = partitions.partition.loc[len(partitions) - 1]
    return last_partition


def get_partitions_to_run(spark, from_table, to_table, from_partition_col='data_date', to_partition_col='data_date'):
    """ 对照两张表的分区差异 返回分区差异的值
    :param spark: SparkSession
    :param from_table: hive table name
    :param to_table: hive table name
    :param from_partition_col: hive partition name(default:data_date)
    :param to_partition_col: hive partition name(default:data_date)
    :return: list
    """
    from_table_par_df = get_partition(spark, from_table, partition_col=from_partition_col)
    to_table_par_df = get_partition(spark, to_table, partition_col=to_partition_col)

    from_table_par = set() if from_table_par_df.empty else \
        set(from_table_par_df[from_partition_col].map(lambda x: x.split("=")[1].strip()))
    to_table_par = set() if to_table_par_df.empty else \
        set(to_table_par_df[to_partition_col].map(lambda x: x.split("=")[1].strip()))

    lack_pars = from_table_par - to_table_par
    return sorted(list(lack_pars))


def add_corrupt_record_col_if_not_exists(schema, corrupt_record_col_name):
    """ 确保schema中有处理corrupt records的column
    :param schema:
    :param corrupt_record_col_name: str
    :return: None, side-effect only (mutate schema)
    """
    if corrupt_record_col_name not in schema.names:
        schema.add(corrupt_record_col_name, StringType())


def clean_table(spark, table, partition_retention):
    """ 清除小时数据, 只保留partition_retention个分区, partition_retention=0会清除所有数据
    :param spark:
    :param table:
    :param partition_retention:
    :return:
    """
    partitions = get_partition(spark, table)  # type: pd.DataFrame
    to_clean_par = partitions if partition_retention == 0 else partitions.head(-partition_retention)
    if not to_clean_par.empty:
        drop_table_partitions(spark, table, to_clean_par.partition)


# noinspection PyPep8Naming,PyIncorrectDocstring
def insert_into_partition(self, tableName, partitionCol, partition, overwrite=False):
    # 注入到sparkSession的方法, 变量命名按照pyspark的大小写
    """ Inserts the content of the :class:`DataFrame` to the specified table partition.

    It requires that the schema of the class:`DataFrame` is the same as the
    schema of the table partition.

    Optionally overwriting any existing data.
    :param tableName:
    :param partitionCol:
    :param partition:
    :param overwrite:
    :return:
    """
    df = self._df
    tmp_table_name = "__tbl_par_to_write" + uuid.uuid4().get_hex()
    insertion_sql = get_insert_partition_table_sql(tmp_table_name, tableName, partitionCol, partition, overwrite)

    df.createOrReplaceTempView(tmp_table_name)
    self._spark.sql(insertion_sql)
    self._spark.dropTempTable(tmp_table_name)


def days_after(days, data_date=None):
    """
    :param data_date: None or str, format:%Y%m%d. e.g. 20180604
    :param days: int
    :return: str, format:%Y%m%d. e.g. 20180604
    """
    date_fmt = "%Y%m%d"
    t = datetime.today() if not data_date else datetime.strptime(data_date, date_fmt)
    t_n = t + timedelta(days=days)
    return t_n.strftime(date_fmt)


def data_date_range(start, end, closed='left'):
    """
    :param start:
    :param end:
    :param closed: 'left'/'right'/None default: 'left', 包括start, 不包括end
    :return:
    """
    return [str(date) for date in pd.date_range(start, end, closed=closed).strftime('%Y%m%d')]


def is_partition_exists(spark, table_name, partition_spec):
    pars = get_partition(spark, table_name)
    return partition_spec in pars.partition.values


def is_data_date_exists(spark, table_name, data_date):
    par_spec = "data_date={}".format(data_date)
    par_exists = is_partition_exists(spark, table_name, par_spec)
    if not par_exists:
        error_msg = "{table} partition ({par_spec}) not exists.".format(
            table=table_name, par_spec=par_spec)
        logging.error(error_msg)
    return par_exists


def take_row_number_less_than_or_equal_to(df, partition_by, order_by, less_than_or_equal_to, row_number_col_name=None):
    # type: (DataFrame, [str], [str], int, None or str) -> DataFrame
    """
    :param df: DataFrame
    :param partition_by: [column name string]
    :param order_by: [order spec string]
    :param less_than_or_equal_to: int, row_number() <= less_than_or_equal_to
    :return: filtered DataFrame
    :param row_number_col_name: None or str, if None, row_number column will not be selected in result DataFrame
    """
    origin_cols = df.columns
    rn_col_name = row_number_col_name if row_number_col_name else "rn_" + uuid.uuid4().get_hex()
    row_number_col = expr(
        "row_number() over (PARTITION BY {par_spec} ORDER BY {order_spec})".format(
            par_spec=",".join(partition_by),
            order_spec=",".join(order_by)
        )
    ).alias(rn_col_name)
    return df.select('*', row_number_col).where(expr(rn_col_name) <= less_than_or_equal_to).select(
        *(['*'] if row_number_col_name else origin_cols)
    )


def get_deletion_hours(spark, hive_hour_table, data_date, partition_column="data_hour"):
    partition_df = get_partition(spark, hive_hour_table)['partition']
    partition_column_df = partition_df.map(
        lambda x: re.compile(partition_column + "=(\d+)", flags=re.IGNORECASE).findall(x)[0])
    partition_date_df = partition_column_df.map(lambda x: str(x) if str(x).startswith(str(data_date)) else False)
    partition_filtered_df = DataFrame({"data_hour": partition_date_df[partition_date_df != False]})

    right_date_array = [data_date + ('0' + str(i) if len(str(i)) == 1 else str(i)) for i in range(0, 24)]
    right_date_df = DataFrame({"data_hour_right": right_date_array})

    # result_df = right_date_df.join(partition_filtered_df,  lsuffix='_caller', rsuffix='_other')
    result_df = pd.merge(right_date_df, partition_filtered_df, left_on='data_hour_right', right_on='data_hour',
                         how='left')
    deletion_hour = result_df.ix[result_df.data_hour.isnull()]['data_hour_right'].tolist()
    return deletion_hour


def wait_for_sync_data(task_name, skip_empty, *data_times):
    task_name_to_task_id = {'online_user': '1'}  # TODO 改为直接使用task_name接口, 否则每个业务都需要向这个字典注册
    headers = {'Authorization': 'Basic ZHBfZXRsOlNqazlpZnZMT2k=', 'Content-Type': 'application/json'}
    # INIT = 0  初始化状态
    # DONE = 1  当前阶段任务完成
    # FAILED = 2 失败
    # FINISHED = 3 任务完成
    # STOPPED = 4 源数据不存在
    for data_time in data_times:
        while True:
            url = 'http://kangaroos-api.jpushoa.com/schedules/{task_id}/tasks?schedule_time={data_time}'.format(
                task_id=task_name_to_task_id.get(task_name),
                data_time=data_time
            )
            res = requests.get(url, headers=headers)
            result = res.json()
            if not result.get('data', ""):  # kangaroos-api 401 403 404 ...
                msg = (result.get("msg", "") or result.get("message", "")).encode("utf-8")
                err_msg = " ".join([str(data_time), 'kangaroos-api:', msg])
                # 中文UTF-8 raise RuntimeError 的时候有问题, 需要转成str, 数字字母UTF-8没问题
                raise Exception(err_msg)
            else:
                status = result['data'][0]['status'].encode("utf-8")
                if status in ['INIT', 'DONE']:
                    logging.warn(str(data_time) + ' wait for file sync')
                    sleep(60 * 10)
                elif status == 'FINISHED':
                    logging.info(str(data_time) + ' ' + status)
                    break
                elif status == 'STOPPED':
                    err_msg = str(data_time) + ' kangaroos-api: no data'
                    if skip_empty:
                        logging.info(err_msg)
                        break  # can be skipped
                    else:  # empty is wrong
                        raise Exception(err_msg)
                else:
                    err_msg = " ".join([str(data_time), 'kangaroos-api:', status])
                    raise Exception(err_msg)


def retry(on_exception, retry_interval_attr_name, max_retry_attr_name):
    def real_decorator(method):
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            retry_interval = getattr(self, retry_interval_attr_name)
            max_retry = getattr(self, max_retry_attr_name)
            assert retry_interval >= 0
            assert max_retry >= 0

            ex = None
            for i in range(max_retry + 1):  # add 1 for the first time (not count as "retry")
                if i != 0:  # is retry
                    logging.warn("waiting for next retry ...")
                    sleep(retry_interval)
                    logging.warn("==== retry times: {i} ====".format(i=i))
                try:
                    return method(self, *args, **kwargs)
                except on_exception as e:
                    logging.warn(str(e))
                    ex = e

            # all retry failed
            if max_retry > 0:
                logging.warn("max retries exceeded")
            error_msg = str(ex)
            # send_alert(u"错误", error_msg, code=self.alert_code)
            raise ex

        return wrapper

    return real_decorator


def get_input_size(read_base_path, data_time, spark):
    """ get input total size in bytes
    :param read_base_path: ','分割路径字符串, 可包含多个路径
    :param data_time: string,
    :param spark: SparkSession
    :return: long/int, total size in bytes
    """
    input_paths = get_valid_paths(spark, read_base_path, data_time)
    input_size = sum([dfs_du_s(p, spark) for p in input_paths])
    logging.info("input {paths} size: {input_size}".format(paths=input_paths, input_size=input_size))
    return input_size


def estimate_expansion_rate(spark, read_base_path, data_time, output_table, partition_col):
    """ 计算原始数据到hive表文件大小的膨胀率
    >>> estimate_expansion_rate(
    >>>     spark, read_base_path="/user/log/newReg/", data_time="2019111112",
    >>>     output_table="edw.register_user_latest_hour_log", partition_col="data_hour"
    >>> )
    >>> 0.31323836540227595
    :param spark: SparkSession
    :param read_base_path: ','分割路径字符串, 可包含多个路径
    :param data_time: string,
    :param output_table: string
    :param partition_col: string
    :return: float
    """
    input_size = get_input_size(read_base_path, data_time, spark)
    output_path = get_table_location(spark, table_name=output_table, partition_spec=partition_col + "=" + data_time)
    output_size = dfs_du_s(output_path, spark)
    return float(output_size)/input_size


def estimate_output_partition_num(spark, read_base_path, data_time, expansion_rate, min_output_file_size=1024**3/2):
    """
    根据膨胀率计算输出文件大小
    :param spark: SparkSession
    :param read_base_path: ','分割路径字符串, 可包含多个路径
    :param data_time: string,
    :param expansion_rate: float
    :param min_output_file_size: long/int, default: 0.5GB
    :return: int
    """
    input_size = get_input_size(read_base_path, data_time, spark)
    est_output_size = input_size * expansion_rate
    est_output_par_num = max(1, int(est_output_size / min_output_file_size))
    return est_output_par_num

