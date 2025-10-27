# -*- coding: utf-8 -*-

"""
descr: pyspark demo
auther: lj.michale
create_date: 2025/9/27 15:54
file_name: pyspark_demo.py
--------------------------------------------------
spark-submit \
--master local[5] \
/export/data/shell/05.SparkSubmit.py \
hdfs://hadoop01:9000/pydata/input/words.txt
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
    df = spark.createDataFrame([("Hello, World!",)], ["message"])

    # ##################################### tansform


    # ##################################### sink
    df.show()

    spark.stop()