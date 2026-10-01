"""Illustrative Spark transformations for bronze, silver, and gold stages."""

from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, current_timestamp


def ingest_bronze(spark: SparkSession, source_path: str, catalog: str) -> None:
    source = spark.read.format("json").load(source_path)
    (source.withColumn("_ingested_at", current_timestamp())
     .write.format("delta").mode("append")
     .saveAsTable(f"{catalog}.bronze.raw_events"))


def transform_silver(spark: SparkSession, catalog: str) -> None:
    bronze = spark.table(f"{catalog}.bronze.raw_events")
    valid = bronze.filter(col("event_id").isNotNull()).dropDuplicates(["event_id"])
    (valid.write.format("delta").mode("overwrite")
     .option("overwriteSchema", "true")
     .saveAsTable(f"{catalog}.silver.events"))


def publish_gold(spark: SparkSession, catalog: str) -> None:
    silver: DataFrame = spark.table(f"{catalog}.silver.events")
    gold = silver.groupBy("event_type").count()
    (gold.write.format("delta").mode("overwrite")
     .saveAsTable(f"{catalog}.gold.event_counts"))

