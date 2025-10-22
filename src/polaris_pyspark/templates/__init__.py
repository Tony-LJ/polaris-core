# -*- coding: utf-8 -*-

"""
命名处理, SQL模板相关
"""
from textwrap import dedent
corrupt_record_col_name = '_corrupt_record'


def strip_meaningless_suffixes(s, meaningless_suffixes=("_log", "_info")):
    """ strip all meaningless suffixes
    :param s: str
    :param meaningless_suffixes: list of str
    :return: str

    >>> strip_meaningless_suffixes("ding_log_business_info_log_info_log")
    'ding_log_business'
    """
    strip_flag = True
    while strip_flag:
        strip_flag = False
        for suffix in meaningless_suffixes:
            if s.endswith(suffix):
                s = s[:-len(suffix)]
                strip_flag = True
    return s


def get_corrupt_record_table_creation_sql(table_name, table_author, table_path=None):
    """ get corrupt record hive table creation SQL statement
    :param table_author:
    :param table_name: str, corrupt_record_table_name
    :param table_path: str, optional, if not given, derive path from table_name
    :return: corrupt record hive table creation SQL statement
    """
    table_path = table_path if table_path else get_external_table_path(table_name)
    table_creation_stmt = dedent("""\
    CREATE EXTERNAL TABLE IF NOT EXISTS {table_name} (
      corrupt_record string
    ) PARTITIONED BY (
      data_hour bigint COMMENT 'data_hour format is yyyyMMddHH'
    ) STORED AS TEXTFILE LOCATION '{table_path}'
    TBLPROPERTIES ('AUTHOR'='{table_author}')
    """).format(table_name=table_name, table_author=table_author, table_path=table_path)
    return table_creation_stmt


data_hour_partition_spec = "data_hour bigint COMMENT 'data_hour format is yyyyMMddHH'"
data_date_partition_spec = "data_date bigint COMMENT 'data_date format is yyyyMMdd'"


def get_decrypt_table_creation_sql(table_name, col_names, partition_col, table_author, table_path=None):
    """ get decrypt hive table creation SQL statement
    :param table_author:
    :param table_name: str
    :param col_names: list of str
    :param partition_col: str, "date_hour" or "date_date"
    :param table_path: str
    :return: str, creation sql statement
    """
    assert len(set(map(col_to_md5_col_name, col_names))) == len(col_names), "col_names中有重名列 {}".format(col_names)
    if partition_col is "data_hour":
        partition_field_spec = data_hour_partition_spec
    elif partition_col is "data_date":
        partition_field_spec = data_date_partition_spec
    else:
        raise NotImplementedError

    decrypt_table_name = get_decrypt_table_name(table_name)
    table_path = table_path if table_path else get_external_table_path(decrypt_table_name)
    md5_fields = map(col_to_md5_col_name, col_names)
    raw_fields = map(col_to_raw_col_name, col_names)
    md5_fields_specs = map("  {} string COMMENT 'md5 hash字段'".format, md5_fields)
    raw_fields_specs = map("  {} string COMMENT '未处理字段'".format, raw_fields)
    fields_spec = ",\n".join(md5_fields_specs + raw_fields_specs)
    table_creation_stmt = dedent("""\
    CREATE EXTERNAL TABLE IF NOT EXISTS {table_name} (
    {fields_spec}
    ) PARTITIONED BY (
      {partition_field_spec}
    ) STORED AS PARQUET LOCATION '{table_path}'
    TBLPROPERTIES ('PARQUET.COMPRESS'='SNAPPY', 'AUTHOR'='{table_author}')
    """).format(table_name=decrypt_table_name, table_path=table_path, table_author=table_author,
                fields_spec=fields_spec, partition_field_spec=partition_field_spec)
    # TODO AUTHOR=...
    return table_creation_stmt


def col_to_md5_col_name(col_name, md5_suffix="_md5"):
    """ add md5_suffix if not end with it
    :param col_name: str
    :param md5_suffix: str
    :return: str
    """
    return col_name if col_name.endswith(md5_suffix) else col_name + md5_suffix


def col_to_raw_col_name(col_name, md5_suffix="_md5"):
    """ strip md5_suffix if end with it
    :param col_name: str
    :param md5_suffix: str
    :return: str
    """
    return col_name[:-len(md5_suffix)] if col_name.endswith(md5_suffix) else col_name


def get_external_table_path(hive_external_table):
    """ get hive external table path by convention
    :param hive_external_table: str
    :return: str, hive external table path by convention
    """
    return "/user/hive/external/{}".format(hive_external_table.replace(r'.', r'/'))


def get_decrypt_table_name(table_name, db_name='secret'):
    """ 解密表表名
    :param table_name: str
    :return: str
    """
    table_name = table_name.replace(table_name.split('.')[0], db_name) if db_name else table_name
    return "{}_decrypt".format(table_name)


def get_corrupt_table_name(table_name):
    """ 坏原始上报表
    :param table_name: str
    :return: str
    """
    return "{}_corrupt_raw".format(table_name)


def get_decrypt_data_table_insertion_sql(data_table, source_table, md5_columns, data_time, partition_col='data_hour'):
    """ get decrypt hive hour table insert SQL statement
    :param data_table: str
    :param source_table: str
    :param md5_columns: list of str
    :param data_time: str
    :param partition_col: str
    :return: str
    """
    md5_fields_specs = [
        "  md5({col}) AS {md5_col_name}".format(col=col, md5_col_name=col_to_md5_col_name(col))
        for col in md5_columns
    ]
    raw_fields_specs = [
        "  {col} AS {raw_col_name}".format(col=col, raw_col_name=col_to_raw_col_name(col))
        for col in md5_columns
    ]
    fields_spec = ",\n".join(md5_fields_specs + raw_fields_specs)
    group_exprs = ", ".join(md5_columns)
    partition_insertion_sql = dedent("""\
    INSERT OVERWRITE TABLE {data_table} PARTITION ({partition_col}={data_time})
    SELECT
    {fields_spec}
    FROM {source_table}
    GROUP BY {group_exprs}
    """).format(
        data_table=data_table, data_time=data_time, fields_spec=fields_spec, partition_col=partition_col,
        source_table=source_table, group_exprs=group_exprs
    )
    return partition_insertion_sql


def get_decrypt_hour_table_insertion_sql(hour_table, source_table, md5_columns, hour):
    """ get decrypt hive hour table insert SQL statement
    :param hour_table: str
    :param source_table: str
    :param md5_columns: list of str
    :param hour: str
    :return: str
    """
    get_decrypt_data_table_insertion_sql(hour_table, source_table, md5_columns, hour, partition_col='data_hour')


def get_hour_to_day_etl_sql(from_table, to_table, cols, data_date, distinct_row=False,
                            old_partition_col="data_hour", new_partition_col="data_date"):
    """ get hour to day etl SQL statement
    :param from_table: str
    :param to_table: str
    :param cols: list of str
    :param data_date: str
    :param distinct_row: bool
    :param old_partition_col: str
    :param new_partition_col: str
    :return: str, SQL stmt
    """
    if old_partition_col and old_partition_col in cols:
        cols.remove(old_partition_col)
    cols_specs = ", ".join(cols)
    group_by_clause = "GROUP BY {}".format(cols_specs) if distinct_row else ""
    sql = dedent("""\
    INSERT OVERWRITE TABLE {to_table} PARTITION ({new_partition_col}={data_date})
    SELECT {cols_specs}
    FROM {from_table}
    WHERE {old_partition_col} like '{data_date}%'
    {group_by_clause}""".format(
        from_table=from_table, to_table=to_table, cols_specs=cols_specs,
        old_partition_col=old_partition_col, new_partition_col=new_partition_col,
        data_date=data_date, group_by_clause=group_by_clause
    ))
    return sql


def get_insert_partition_table_sql(from_table, to_table, partition_col, partition, overwrite=False):
    sql = "INSERT {into} TABLE {to_table} PARTITION ({partition_col}={partition})\n" \
          "select * from {from_table}".format(
        from_table=from_table, to_table=to_table, partition_col=partition_col, partition=partition,
        into="OVERWRITE" if overwrite else "INTO"
    )
    return sql


def get_hour_to_day_et_sql(from_table, cols, data_date, distinct_row=False,
                            old_partition_col="data_hour"):
    """ get hour to day ET (ETL without Load) SQL statement
    :param from_table: str
    :param to_table: str
    :param cols: list of str
    :param data_date: str
    :param distinct_row: bool
    :param old_partition_col: str
    :param new_partition_col: str
    :return: str, SQL stmt
    """
    if old_partition_col and old_partition_col in cols:
        cols.remove(old_partition_col)
    cols_specs = ", ".join(cols)
    group_by_clause = "GROUP BY {}".format(cols_specs) if distinct_row else ""
    sql = dedent("""\
    SELECT {cols_specs}
    FROM {from_table}
    WHERE {old_partition_col} like '{data_date}%'
    {group_by_clause}""".format(
        from_table=from_table, cols_specs=cols_specs,
        old_partition_col=old_partition_col,
        data_date=data_date, group_by_clause=group_by_clause
    ))
    return sql
