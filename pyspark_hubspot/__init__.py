from .hubspot import HubspotDataSource
from pyspark.sql import SparkSession

spark = SparkSession.getActiveSession()
if spark:
    spark.dataSource.register(HubspotDataSource)