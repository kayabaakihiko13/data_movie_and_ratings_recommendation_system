from pyspark.sql import SparkSession

spark=SparkSession\
    .builder \
    .appName("Run utils")\
    .config("spark.some.config.option",'some-value')\
    .getOrCreate()
