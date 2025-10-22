#! /usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os
from datetime import datetime, timedelta

from pyspark.sql.types import StringType
from .templates import (get_corrupt_record_table_creation_sql,
                        get_decrypt_table_creation_sql,
                        get_decrypt_table_name,
                        corrupt_record_col_name,
                        get_corrupt_table_name)
from utils import (hour_to_day_etl,
                   get_partition,
                   dfs_ls,
                   add_corrupt_record_col_if_not_exists,
                   init_spark,
                   clean_table,
                   periodic_etl,
                   get_deletion_hours,
                   wait_for_sync_data,
                   retry)


class Cli(object):
    """
    基于spark4.x的pyspark etl开发框架
    """
    def __init__(
        self,
        app_name,
        yarn_queue,
        read_base_path,
        read_data_schema,
        hive_table_author,
        hive_hour_table,
        hive_hour_table_schema,
        hive_day_table,
        hive_day_table_schema,
        transform,
        hour_table_partition_retention,
        alert_code,
        md5_columns=(),
        corrupt_record_cnt_alert=True,
        corrupt_record_cnt_alert_threshold=0,
        corrupt_record_cnt_fail_threshold=2000,
        distinct_row=False,
        partition_col="data_hour",
        time_type='Hour',
        transform_day=None,
        file_type='json',
        read_args=None,
        check_sync_data=False,
        skip_empty_read_path=True,
        use_cache=True,
        hour_etl_max_retry=0,
        hour_etl_retry_interval=600,
        day_etl_max_retry=0,
        day_etl_retry_interval=600,
        enable_hbo=True,
        min_output_file_size=1024**3/2
    ):
        """
        :param app_name: string
        :param yarn_queue: string
        :param read_base_path: string, path of raw json/csv/... file
        :param read_data_schema: StructType
        :param hive_table_author: string, hive table author
        :param hive_hour_table: string, hive hour table name
        :param hive_hour_table_schema: string
        :param hive_day_table: string
        :param hive_day_table_schema: string
        :param transform: function: DataFrame -> DataFrame
        :param hour_table_partition_retention: int
        :param alert_code: int
        :param md5_columns: list of str
        :param corrupt_record_cnt_alert: bool
        :param corrupt_record_cnt_alert_threshold: int
        :param corrupt_record_cnt_fail_threshold: int
        :param distinct_row: string
        :param partition_col: string
        :param time_type: string (TODO)
        :param transform_day: function: DataFrame -> DataFrame
        :param file_type: str, "json" or "csv"
        :param read_args: dict, other args for spark.read.csv or spark.read.json
        :param check_sync_data: bool
        :param skip_empty_read_path: bool, if False, raise Exception when not data in read path
        :param use_cache: read/parse json only once
        :param hour_etl_max_retry: int, 0 means no retry
        :param hour_etl_retry_interval: int, seconds
        :param day_etl_max_retry: int, 0 means no retry
        :param day_etl_retry_interval: int, seconds
        :param enable_hbo: bool, enable history based optimization flag
        :param min_output_file_size: long/int, default 1024**3/2 bytes (0.5GB)
        """
        self.app_name = app_name
        self.yarn_queue = yarn_queue
        self.hive_table_author = hive_table_author
        self.partition_col = partition_col
        self.time_type = time_type
        # spark接受的SQL不能以';'结尾, 截掉结尾';'
        self._create_table_dict = dict()  # 所有表创建SQL语句
        self.hive_hour_table = hive_hour_table
        if hive_hour_table_schema:
            self.hive_hour_table_schema = hive_hour_table_schema.rstrip().rstrip(';')
            self._create_table_dict[self.hive_hour_table] = self.hive_hour_table_schema
        self.hive_hour_corrupt_record_table = get_corrupt_table_name(hive_hour_table)
        self.hive_hour_corrupt_record_table_schema = get_corrupt_record_table_creation_sql(
            self.hive_hour_corrupt_record_table, self.hive_table_author)
        self._create_table_dict[self.hive_hour_corrupt_record_table] = self.hive_hour_corrupt_record_table_schema
        self.hive_day_table = hive_day_table
        if hive_day_table_schema:
            self.hive_day_table_schema = hive_day_table_schema.rstrip().rstrip(';')
            self._create_table_dict[self.hive_day_table] = self.hive_day_table_schema
        if md5_columns:
            self.hive_hour_decrypt_table = get_decrypt_table_name(hive_hour_table)
            self.hive_hour_decrypt_table_schema = get_decrypt_table_creation_sql(
                hive_hour_table, md5_columns, partition_col=self.partition_col, table_author=self.hive_table_author
            )
            self._create_table_dict[self.hive_hour_decrypt_table] = self.hive_hour_decrypt_table_schema
            self.hive_day_decrypt_table = get_decrypt_table_name(hive_day_table)
            self.hive_day_decrypt_table_schema = get_decrypt_table_creation_sql(
                hive_day_table, md5_columns, partition_col="data_date", table_author=self.hive_table_author
            )
            self._create_table_dict[self.hive_day_decrypt_table] = self.hive_day_decrypt_table_schema
        for table, creation_sql in self._create_table_dict.items():
            assert (table in creation_sql), "table name not match with creation_sql"

        self.md5_columns = md5_columns

        # 所有小时表
        self.hour_tables = [self.hive_hour_table, self.hive_hour_corrupt_record_table] + \
                           ([self.hive_hour_decrypt_table] if md5_columns else [])
        # 所有天表
        self.day_tables = [self.hive_day_table] + ([self.hive_day_decrypt_table] if md5_columns else [])
        # 小时表和天表之间对应关系
        self.hour_table_to_day_table = {self.hive_hour_table: self.hive_day_table}
        if md5_columns:
            self.hour_table_to_day_table[self.hive_hour_decrypt_table] = self.hive_day_decrypt_table

        self.read_base_path = read_base_path
        self.read_data_schema = read_data_schema
        # 确保schema中有处理corrupt records的column
        self.column_name_of_corrupt_record = corrupt_record_col_name
        add_corrupt_record_col_if_not_exists(read_data_schema,corrupt_record_col_name=self.column_name_of_corrupt_record)

        self.transform = transform
        self.hour_table_partition_retention = hour_table_partition_retention
        self.alert_code = alert_code
        self.corrupt_record_cnt_alert = corrupt_record_cnt_alert
        self.corrupt_record_cnt_alert_threshold = corrupt_record_cnt_alert_threshold
        self.corrupt_record_cnt_fail_threshold = corrupt_record_cnt_fail_threshold
        self.distinct_row = distinct_row

        self._udfs = []
        self._java_udfs = []
        self.debug = False
        self._spark = None  # lazy init
        self.transform_day = transform_day
        self.file_type = file_type
        self.read_args = read_args if read_args else {}  # default: {}
        self.etl_time = ''  # 清洗时间
        self.check_sync_data = check_sync_data
        self.skip_empty_read_path = skip_empty_read_path
        self.use_cache = use_cache
        self.hour_etl_max_retry = hour_etl_max_retry
        self.hour_etl_retry_interval = hour_etl_retry_interval
        self.day_etl_max_retry = day_etl_max_retry
        self.day_etl_retry_interval = day_etl_retry_interval

        self.enable_hbo = enable_hbo
        self.min_output_file_size = min_output_file_size

    def __del__(self):
        if self._spark:
            self._spark.stop()

    def register_udf(self, name, f, returnType=StringType()):
        """
        wrapper of spark.udf.register
        :param name:
        :param f:
        :param returnType:
        :return:
        """
        # returnType这个命名是为了兼容spark.udf.register的signature, 没有不一致的必要
        self._udfs.append({"name": name, "f": f, "returnType": returnType})
        return self

    # noinspection PyPep8Naming
    def register_java_udf(self, name, javaClassName, returnType=StringType()):
        """
        wrapper of spark.udf.registerjavaFunction
        :param name:
        :param javaClassName:
        :param returnType:
        :return:
        """
        # returnType这个命名是为了兼容spark.udf.register的signature, 没有不一致的必要
        self._java_udfs.append({"name": name, "javaClassName": javaClassName, "returnType": returnType})
        return self

    def __get_or_init_spark(self):
        if not self._spark:
            spark = init_spark(self.app_name, self.yarn_queue)
            # register udfs
            for udf_spec in self._udfs:
                spark.udf.register(**udf_spec)

            for java_udf_spec in self._java_udfs:
                spark.registerJavaFunction(**java_udf_spec)
            self._spark = spark
        return self

    def create_hive_tables(self, dry_run=False):
        """
        :param dry_run: bool, if True, just print creation SQLs
        :return:
        """
        if dry_run:
            for table in sorted(self._create_table_dict.keys()):  # 按表名顺序输出
                print(self._create_table_dict[table] + ";\n")  # ends with ';'
        else:
            self.__get_or_init_spark()
            for table in sorted(self._create_table_dict.keys()):
                creation_sql = self._create_table_dict[table]
                print("creating table: " + table)
                self._spark.sql(creation_sql)

            # 检查hour_table和day_table的schema是否一致
            hour_table_fields = self._spark.table(self.hive_hour_table).schema.names
            hour_table_fields.remove('data_hour')
            day_table_fields = self._spark.table(self.hive_day_table).schema.names
            day_table_fields.remove('data_date')
            assert set(hour_table_fields) == set(day_table_fields), "inconsistent schema"

    def data_etl(self, *data_times):
        """
         data_etl
        :param data_times:
        :return:
        """
        if self.check_sync_data:
            # 检查跨机房同步数据，延迟情况
            wait_for_sync_data(self.app_name, self.skip_empty_read_path, *data_times)

        self.__get_or_init_spark()  # lazy init
        for data_time in data_times:
            data_time = str(data_time)
            self.etl_time = data_time
            logging.warn("---- {time_type} ETL: ".format(time_type=self.time_type) + data_time)
            try:
                corrupt_cnt = periodic_etl(
                    spark=self._spark,
                    read_base_path=self.read_base_path,
                    read_data_schema=self.read_data_schema,
                    data_table=self.hive_hour_table,
                    data_time=data_time,
                    transform=self.transform,
                    column_name_of_corrupt_record=self.column_name_of_corrupt_record,
                    data_corrupt_record_table=self.hive_hour_corrupt_record_table,
                    debug=self.debug,
                    md5_columns=self.md5_columns,
                    partition_col=self.partition_col,
                    file_type=self.file_type,
                    read_args=self.read_args,
                    skip_empty_read_path=self.skip_empty_read_path,
                    use_cache=self.use_cache,
                    enable_hbo=self.enable_hbo,
                    min_output_file_size=self.min_output_file_size
                )
                if corrupt_cnt > 0:
                    warn_msg = "{time_type} Data ETL warning: {table_name} where ({partition_col}={data_time}) " \
                               "#(corrupt_record)={cnt}".format(
                        table_name=self.hive_hour_corrupt_record_table, time_type=self.time_type,
                        data_time=data_time, cnt=corrupt_cnt, partition_col=self.partition_col)
                    logging.warn(warn_msg)
                    if self.corrupt_record_cnt_alert and corrupt_cnt > self.corrupt_record_cnt_alert_threshold:
                        print(warn_msg)
                        # send_alert(u"警告", warn_msg, code=self.alert_code)
                    if corrupt_cnt > self.corrupt_record_cnt_fail_threshold:
                        raise Exception("Too many corrupt records")
            except Exception as ex:
                logging.exception(ex)
                read_path = os.path.join(self.read_base_path, data_time)
                error_msg = "{time_type} Data ETL failed. {table_name}: {read_path}".format(
                    time_type=self.time_type, table_name=self.hive_hour_table, read_path=read_path)
                raise Exception(error_msg)

    @retry(on_exception=Exception, retry_interval_attr_name="hour_etl_retry_interval",
           max_retry_attr_name="hour_etl_max_retry")
    def hour_etl(self, *data_hours):
        self.data_etl(*data_hours)

    @retry(on_exception=Exception, retry_interval_attr_name="day_etl_retry_interval",
           max_retry_attr_name="day_etl_max_retry")
    def day_etl(self, *data_dates):
        self.__get_or_init_spark()  # lazy init

        for data_date in data_dates:
            data_date = str(data_date)
            logging.warn("==== Day ETL {}: {}".format(self.hive_day_table, data_date))
            try:
                if self.check_sync_data or not self.skip_empty_read_path:
                    deletion_hour = get_deletion_hours(self._spark, self.hive_hour_table, data_date)  # TODO 函数名乱取
                    if deletion_hour:  # TODO 变量名乱取
                        logging.warn(
                            "The hive table {hive_hour_table} deletion some hours: {deletion_hour}, start running deletion hours data..".format(
                                hive_hour_table=self.hive_hour_table, deletion_hour=deletion_hour))
                        self.hour_etl(*deletion_hour)

                hour_to_day_etl(self._spark,
                                self.hive_hour_table,
                                self.hive_day_table,
                                data_date,
                                distinct_row=self.distinct_row,
                                transform_day=self.transform_day,
                                enable_hbo=self.enable_hbo,
                                min_output_file_size=self.min_output_file_size)
                if self.md5_columns:
                    hour_to_day_etl(
                        self._spark,
                        hour_table=self.hive_hour_decrypt_table,
                        day_table=self.hive_day_decrypt_table,
                        data_date=data_date, distinct_row=True,
                        transform_day=self.transform_day,
                        enable_hbo=self.enable_hbo,
                        min_output_file_size=self.min_output_file_size)
            except Exception as ex:
                logging.exception(ex)
                error_msg = "Day Transform ETL failed. {}: {}".format(self.hive_day_table, data_date)
                raise Exception(error_msg)

        # clean after day etl
        self.clean_hour_data(hour_table_partition_retention=self.hour_table_partition_retention)

    def clean_hour_data(self, hour_table_partition_retention=None):
        """
        清除小时数据, 只保留hour_table_partition_retention个分区, 如果hour_table_partition_retention未指定,
        保留self.hour_table_partition_retention个分区. hour_table_partition_retention=0会清除所有数据
        :param hour_table_partition_retention: int
        :return: None
        """
        partition_retention = hour_table_partition_retention if hour_table_partition_retention is not None \
            else self.hour_table_partition_retention
        assert partition_retention >= 0, "hour_table_partition_retention should >= 0"
        spark = self._spark

        for hour_table in self.hour_tables:
            clean_table(spark, hour_table, partition_retention)

    def _drop_hive_tables(self, clean_all_data=False):
        self.__get_or_init_spark()  # lazy init
        for table in self._create_table_dict.keys():
            if clean_all_data:
                clean_table(self._spark, table, partition_retention=0)
            drop_stmt = 'drop table {table}'.format(table=table)
            logging.warn(drop_stmt)
            self._spark.sql(drop_stmt)

    def tail_partition(self, n=8):
        self.__get_or_init_spark()  # lazy init
        read_path_par_df = dfs_ls(self.read_base_path, self._spark).tail(n)
        print("======== read_path ========")
        print(read_path_par_df.path)
        hour_corrupt_table_par_df = get_partition(self._spark, self.hive_hour_corrupt_record_table).tail(n)
        print("======== {table_name} ========".format(table_name=self.hive_hour_corrupt_record_table))
        print(hour_corrupt_table_par_df)
        hour_table_par_df = get_partition(self._spark, self.hive_hour_table).tail(n)
        print("======== {table_name} ========".format(table_name=self.hive_hour_table))
        print(hour_table_par_df)
        day_table_par_df = get_partition(self._spark, self.hive_day_table).tail(n)
        print("======== {table_name} ========".format(table_name=self.hive_day_table))
        print(day_table_par_df)

    def get_hours_to_run(self,
                         ignore_current_hour=True,
                         ignore_retention=False,
                         hour_window=None,
                         window_end_hour=None):
        """返回最近hour_table_partition_retention个小时原始数据中没有清理为小时表的小时列表
        :param ignore_current_hour: bool, 是否忽略当前小时
        :param ignore_retention: bool, 是否忽略hour_table_partition_retention, 使用全部数据
        :param hour_window: int, 当前小时往前看的小时个数
        :param window_end_hour: str, 配合hour_window使用, hour_window结束时间点(%Y%m%d%H)
        :return: list of hour strings
        """
        # TODO check partition file
        hour_fmt = "%Y%m%d%H"

        self.__get_or_init_spark()  # lazy init
        read_path_par_df = dfs_ls(self.read_base_path, self._spark, sort_by_mtime=False)
        if not ignore_retention:  # take pathes within retention
            read_path_par_df = read_path_par_df.tail(self.hour_table_partition_retention + ignore_current_hour)
        hour_table_par_df = get_partition(self._spark, self.hive_hour_table)

        path_par_list = [] if read_path_par_df.empty \
            else list(read_path_par_df.path.str.split(r'/', expand=True).iloc[:, -1])
        # 处理归档路径(.har)
        path_par = {p[:-len(".har")] if p.endswith(".har") else p for p in path_par_list}
        hour_table_par = set() if hour_table_par_df.empty \
            else set(hour_table_par_df.partition.str.split(r'=', expand=True).iloc[:, -1])
        diff_hours = path_par - hour_table_par

        if ignore_current_hour and diff_hours:
            current_hour = datetime.now().strftime(hour_fmt)
            if current_hour in diff_hours:
                diff_hours.remove(current_hour)
            elif min(path_par) in diff_hours:
                diff_hours.remove(min(diff_hours))

        hours = sorted(diff_hours)

        # hour_window & window_end_hour
        if hour_window:
            if not window_end_hour:
                window_end_hour = datetime.now().strftime(hour_fmt)
            end_datetime = datetime.strptime(window_end_hour, hour_fmt)
            start_datetime = end_datetime + timedelta(hours=-hour_window)
            start = format(start_datetime, hour_fmt)
            hours = [h for h in hours if start <= h < window_end_hour]

        return hours

    def get_days_to_run(self, ignore_today=True, back_days=100):
        """
        返回待从小时表清理到天表的天列表
        :param ignore_today: bool, 是否忽略当天
        :param back_days: 天表往回看的分区数
        :return: list of day strings
        """
        # TODO check partition file
        day_fmt = "%Y%m%d"

        self.__get_or_init_spark()  # lazy init
        hour_table_par_df = get_partition(self._spark, self.hive_hour_table)
        day_table_par_df = get_partition(self._spark, self.hive_day_table).tail(back_days)

        hour_table_par = set() if hour_table_par_df.empty \
            else set(hour_table_par_df.partition.str.split(r'=', expand=True).iloc[:, -1])
        hour_table_day_par = {h[:8] for h in hour_table_par}
        day_table_par = set() if day_table_par_df.empty \
            else set(day_table_par_df.partition.str.split(r'=', expand=True).iloc[:, -1])
        diff_days = hour_table_day_par - day_table_par

        if ignore_today and diff_days:
            today = datetime.now().strftime(day_fmt)
            if today in diff_days:
                diff_days.remove(today)

        days = sorted(diff_days)
        return days

    def run_all(self, ignore_retention=False):
        """
        补数据用, 先跑小时表在跑天表
        :param ignore_retention:
        :return:
        """
        hours_to_run = self.get_hours_to_run(ignore_retention=ignore_retention)
        logging.warn("hours_to_run: {hours}".format(hours=hours_to_run))
        self.hour_etl(*hours_to_run)

        days_to_run = self.get_days_to_run()
        logging.warn("days_to_run: {days}".format(days=days_to_run))
        self.day_etl(*days_to_run)
