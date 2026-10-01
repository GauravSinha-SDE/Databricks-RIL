"""Asset Bundle task entry points."""

import argparse
import os

from pyspark.sql import SparkSession


def _args(include_source: bool = False):
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", required=True)
    if include_source:
        parser.add_argument("--source-path", default=os.environ.get("SOURCE_PATH", "/Volumes/main/landing/events"))
    return parser.parse_args()


def ingest_bronze():
    from pipelines.medallion import ingest_bronze as run
    args = _args(include_source=True)
    run(SparkSession.builder.getOrCreate(), args.source_path, args.catalog)


def transform_silver():
    from pipelines.medallion import transform_silver as run
    args = _args()
    run(SparkSession.builder.getOrCreate(), args.catalog)


def publish_gold():
    from pipelines.medallion import publish_gold as run
    args = _args()
    run(SparkSession.builder.getOrCreate(), args.catalog)

