from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("OptimizedJob").getOrCreate()

# Only select needed columns early (projection pushdown)
df = spark.read.parquet("wasbs://data@mycontainer.blob.core.windows.net/patient_records") \
    .select("patient_id", "last_updated", "some_other_column")

# Filter old records early to reduce volume (predicate pushdown)
df = df.filter("last_updated >= '2023-01-01'")

# Cache intermediate data (if reused later)
df.cache()

# Read only needed insurance columns
insurance_df = spark.read.parquet("wasbs://data@mycontainer.blob.core.windows.net/insurance_data") \
    .select("patient_id", "eligibility_status")

# Broadcast join to prevent large shuffle (assumes insurance_df is small)
from pyspark.sql.functions import broadcast
joined = df.join(broadcast(insurance_df), "patient_id")

# Use withColumn for flag
joined = joined.withColumn("eligibility_flag", joined["eligibility_status"] == "eligible")

# Repartition output to reduce small files before writing
joined = joined.repartition(10)

# Write with partitioning for downstream efficiency
joined.write.mode("overwrite").parquet("wasbs://output@mycontainer.blob.core.windows.net/results")
