from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("InefficientJob").getOrCreate()

# Reading full dataset from blob storage
df = spark.read.parquet("wasbs://data@mycontainer.blob.core.windows.net/patient_records")

# Doing a full join with insurance data (no filtering, causes shuffle)
insurance_df = spark.read.parquet("wasbs://data@mycontainer.blob.core.windows.net/insurance_data")

# Wide transformation
joined = df.join(insurance_df, df["patient_id"] == insurance_df["patient_id"])

# Adding new derived column
joined = joined.withColumn("eligibility_flag", joined["eligibility_status"] == "eligible")

# Writing back to storage without partitioning
joined.write.parquet("wasbs://output@mycontainer.blob.core.windows.net/results", mode="overwrite")
