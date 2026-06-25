import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import col

VM_URL = "http://localhost:8428/api/v1/import/prometheus"

spark = SparkSession.builder.appName("CUR-to-VM").getOrCreate()

df = spark.read.parquet("curs")

# --- base cost metrics ---
metrics = []

for row in df.collect():
    region = row["product_region_code"]
    service = row["line_item_product_code"]
    cost = row["line_item_unblended_cost"]

    metrics.append(f'aws_cost_total{{region="{region}",service="{service}"}} {cost}')
    metrics.append(f'aws_cost_region{{region="{region}"}} {cost}')
    metrics.append(f'aws_cost_service{{service="{service}"}} {cost}')

    # GreenOps factor (simple demo model)
    region_factor = {
        "us-east-1": 0.0004,
        "eu-west-1": 0.0002,
    }.get(region, 0.0003)

    co2 = cost * region_factor

    metrics.append(f'aws_co2_estimate{{region="{region}"}} {co2}')

payload = "\n".join(metrics)

response = requests.post(VM_URL, data=payload)

print("Pushed metrics to VictoriaMetrics:", response.status_code)
