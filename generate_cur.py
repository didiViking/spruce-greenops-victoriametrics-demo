from pyspark.sql import SparkSession
from pyspark.sql.functions import lit

spark = SparkSession.builder.appName("CUR").getOrCreate()

data = [
    ("us-east-1", "AmazonEC2", "123456789012", "2026-06-24", "2026-06-24", 0.12),
    ("eu-west-1", "AmazonS3", "123456789012", "2026-06-24", "2026-06-24", 0.03),
]

columns = [
    "product_region_code",
    "line_item_product_code",
    "line_item_usage_account_id",
    "line_item_usage_start_date",
    "line_item_usage_end_date",
    "line_item_unblended_cost",
]

df = spark.createDataFrame(data, columns)

df.write.mode("overwrite").parquet("curs")

print("✔ CUR dataset written to: curs")
