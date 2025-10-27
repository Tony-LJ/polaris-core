# -*- coding: utf-8 -*-

"""
descr: pyspark demo
auther: lj.michale
create_date: 2025/9/27 15:54
-------------------------------------------
部署命令：
$SPARK_HOME/bin/spark-submit --master yarn --deploy-mode client --executor-cores 1 pyspark_demo2.py
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType

def convertCase(str):
    """
    字符串转换
    :param str:
    :return:
    """
    resStr = ""
    arr = str.split(" ")
    for x in arr:
        resStr = resStr + x[0:1].upper() + x[1:len(x)] + " "

    return resStr

def main():
    # hive.metastore.uris: 访问hive metastore 服务的地址
    spark = SparkSession.builder \
        .appName('SparkByTry') \
        .config("hive.metastore.uris", "thrift://10.192.0.71:9083") \
        .enableHiveSupport() \
        .getOrCreate()

    spark.conf.set("spark.sql.execution.arrow.pyspark.enabled", 'true')

    df = spark.createDataFrame([("Scala", 25000), ("Spark", 35000), ("PHP", 21000)])
    df.show()

    # Spark SQL
    df.createOrReplaceTempView("sample_table")
    df2 = spark.sql("SELECT _1,_2 FROM sample_table")
    df2.show()

    # Create Hive table & query it.
    spark.table("sample_table").write.saveAsTable("sample_hive_table")
    df3 = spark.sql("SELECT _1,_2 FROM sample_hive_table")
    df3.show()

    dbs = spark.catalog.listDatabases()
    print(dbs)


if __name__ == '__main__':
    main()