# -*- coding: utf-8 -*-

"""
descr: Python UDF函数样例
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: string_length_udf.py

ADD FILE /usr/kw/string_length_udf.py;
add file hdfs:///tmp/string_length_udf.py

jar cf string_length_udf.jar /usr/kw/string_length_udf.spec

ADD JAR /usr/kw/string_length_udf.jar;
CREATE TEMPORARY FUNCTION string_length AS 'string_length_udf.string_length';
SELECT string_length('Hello, ', 'World!') AS greeting;

"""

def string_length(s):
    """
     计算字符串长度
    :param s:
    :return:
    """
    return len(s)


