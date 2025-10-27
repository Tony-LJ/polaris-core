# -*- coding: utf-8 -*-

"""
descr: pyspark demo
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: pyspark_demo.py
"""
from pyspark.sql import SparkSession
from operator import add


if __name__ == '__main__':
    # #################################
    spark = SparkSession.builder \
        .master("local[*]") \
        .appName("pyspark_demo") \
        .config("spark.driver.memory", "10g") \
        .config("spark.driver.cores", "2") \
        .config("spark.executor.memory", "10g") \
        .config("spark.executor.cores", "2") \
        .enableHiveSupport() \
        .getOrCreate()
    sc = spark.sparkContext

    # ##################################### source
    print(" >>>>>>>>>>>>>>>>>> ")
    lines = spark.read.text("files:///").rdd.map(lambda r: r[0])

    # ##################################### tansform
    counts = (lines.flatMap(lambda x: x.split(' ')) \
              .map(lambda x: (x, 1)) \
              .reduceByKey(add))

    # ##################################### sink
    output = counts.collect()

    spark.stop()