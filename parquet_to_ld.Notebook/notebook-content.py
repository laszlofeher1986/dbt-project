# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "4e081237-3e52-41ae-8a03-1c9e0f13f7c6",
# META       "default_lakehouse_name": "LH_LF",
# META       "default_lakehouse_workspace_id": "6443336d-2e57-4f8f-acbf-3c1fe1869bb4"
# META     }
# META   }
# META }

# CELL ********************

from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StructType, StructField, StringType, DoubleType
from delta import *
from pathlib import Path

# Initialize Spark session with Delta support
spark = SparkSession.builder \
    .appName("Load Parquet to Delta") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .enableHiveSupport() \
    .getOrCreate()

# Define the Fabric Lakehouse directory path
parquet_path = "Files/exchange_rates/*/*/*/*.parquet"
delta_table_name = "ld_exchange_rates"

# Read Parquet files without enforcing schema
raw_df = spark.read.format("parquet").load(parquet_path)

# Print inferred schema to identify data types
print("Inferred Schema:")
raw_df.printSchema()

# Ensure all columns match the expected schema
df = raw_df \
    .withColumn("Date", col("Date").cast(StringType())) \
    .withColumn("0", col("0").cast(StringType())) \
    .withColumn("1", col("1").cast(StringType())) \
    .withColumn("2", col("2").cast(DoubleType())) \
    .withColumn("3", col("3").cast(DoubleType()))

row_count = df.count()
print(f"Loaded {row_count} rows from Parquet.")
df.show(5, truncate=False)

if row_count == 0:
    print("Warning: No data loaded from Parquet files.")
else:
    print(f"Schema used: {df.schema}")

# Enable schema auto-merge to handle future schema changes
spark.conf.set("spark.databricks.delta.schema.autoMerge.enabled", "true")

# Perform UPSERT (MERGE) to avoid duplicates
from delta.tables import DeltaTable

delta_table = DeltaTable.forName(spark, delta_table_name)
delta_table.alias("tgt").merge(
    df.alias("src"),
    "tgt.Date = src.Date AND tgt.`0` = src.`0`"
).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

print(f"Data successfully merged into Delta table: {delta_table_name}")

# Optimize the Delta table for performance
try:
    spark.sql(f"OPTIMIZE {delta_table_name}")
    print(f"Delta table {delta_table_name} optimized successfully.")
except Exception as e:
    print(f"Error optimizing Delta table: {e}")

# Load the Delta table into a DataFrame and display it
try:
    df = spark.read.format("delta").table(delta_table_name)
    row_count = df.count()
    print(f"Loaded {row_count} rows from Delta table.")
    df.show(5, truncate=False)
except Exception as e:
    print(f"Error loading Delta table: {e}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
