# 🌱 GreenOps Observability Demo (CUR → VictoriaMetrics → Grafana)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-demo-orange.svg)
![Stack](https://img.shields.io/badge/stack-spark%20%7C%20victoriametrics%20%7C%20grafana-green.svg)

A GreenOps observability pipeline that transforms AWS Cost and Usage Report (CUR)-like data into cost and carbon metrics, then visualizes them using **VictoriaMetrics + Grafana**.

This project demonstrates how sustainability can be treated as a **first-class observability signal**.

## 🧩 Role of Spruce in this GreenOps Architecture

This project follows a cloud-native observability pattern inspired by open source ecosystem tools, where data generation, processing, and observability are clearly separated into independent layers.

Within this architecture, **Spruce is used strictly as a synthetic data generation and normalization layer**.

What is Spruce? Check it out: 👉 https://opensourcegreenops.cloud/latest/, 👉 https://github.com/digitalpebble/spruce.

---

### 🌱 Spruce as the Data Generation Layer

Spruce acts as a reproducible pipeline that simulates an AWS Cost and Usage Report (CUR)-like dataset using Apache Spark.

Its responsibilities in this demo are:

- Generating synthetic CUR-like cost and usage data
- Applying basic normalization and structuring of cloud billing fields
- Producing a columnar dataset in **Parquet format**
- Emitting a dataset compatible with downstream observability pipelines

The resulting dataset represents a simplified but realistic approximation of cloud billing telemetry, typically found in enterprise FinOps environments.

---

### 📦 Output Contract

Spruce produces a structured dataset containing cloud usage and cost attributes such as:

- `product_region_code`
- `line_item_product_code`
- `line_item_usage_account_id`
- `line_item_usage_start_date`
- `line_item_usage_end_date`
- `line_item_unblended_cost`

This dataset acts as the **source of truth for downstream GreenOps metrics generation**.

---

### 🚫 What Spruce is NOT Responsible For

To maintain clear separation of concerns, Spruce does not participate in:

- Metrics generation (Prometheus/VictoriaMetrics format)
- Time-series ingestion or storage
- Carbon intensity calculations
- Observability visualization (Grafana dashboards)
- Any form of alerting or querying layer

---

### 🔄 Downstream Flow

After Spruce completes dataset generation, the pipeline continues as follows:

1. **Spruce (Batch Processing Layer)**
   - Produces CUR-like Parquet dataset

2. **Python Transformation Layer (Metrics Adapter)**
   - Converts cost data into Prometheus-compatible metrics
   - Aggregates by service, region, and account
   - Enriches metrics with CO₂ emission factors

3. **VictoriaMetrics (Observability Storage Layer)**
   - Stores time-series cost and carbon metrics
   - Provides PromQL-compatible query interface

4. **Grafana (Visualization Layer)**
   - Displays GreenOps dashboards
   - Enables cost and carbon observability across services

---

### 🧭 Design Principle

This architecture follows a typical separation of concerns:

- **Batch/Data Generation Layer → Spruce**
- **Metrics Transformation Layer → Python exporter**
- **Time-Series Storage Layer → VictoriaMetrics**
- **Visualization Layer → Grafana**

This separation ensures the system remains:
- Modular
- Reproducible
- Observability-native
- Vendor-neutral

---

### 🌍 In this GreenOps demo:

- Spruce is the **data plane simulator**
- VictoriaMetrics is the **metrics backbone**
- Grafana is the **insight layer**

Together, they form a lightweight cloud-native observability pipeline for cost and carbon intelligence.

---

## 🏗️ Architecture

```text
┌──────────────────────┐
│   CUR (Spark job)    │
└─────────┬────────────┘
          ↓
┌──────────────────────┐
│  Parquet dataset     │
└─────────┬────────────┘
          ↓
┌──────────────────────┐
│ Python metric export │
│ (CUR → Prom metrics) │
└─────────┬────────────┘
          ↓
┌──────────────────────┐
│ VictoriaMetrics      │
└─────────┬────────────┘
          ↓
┌──────────────────────┐
│ Grafana dashboards   │
└──────────────────────┘

```

---

## 📊 Metrics Model

### 💰 Cost metrics

- `aws_cost_total`
- `aws_cost_service`
- `aws_cost_region`

### 🌍 Carbon metric

- `aws_co2_estimate`

Derived from:

aws_co2_estimate = aws_cost_total × region_emission_factor

---

## 📁 Repository structure

```text
spruce-greenops-vm-demo/
┌──────────────────────────────┐
│ generate_cur.py             │
│ (Spark CUR generator)       │
└──────────────┬───────────────┘
               │
┌──────────────▼───────────────┐
│ cur_to_victoriametrics.py   │
│ (CUR → Prometheus metrics)  │
└──────────────┬───────────────┘
               │
┌──────────────▼───────────────┐
│ grafana/                    │
│ └── dashboard.json          │
└──────────────┬───────────────┘
               │
┌──────────────▼───────────────┐
│ curs/                       │
│ ├── part-*.parquet          │
│ └── _SUCCESS                │
└──────────────┬───────────────┘
               │
┌──────────────▼───────────────┐
│ output/                     │
│ (optional artifacts)        │
└──────────────────────────────┘
```

---

## 🚀 Getting Started

---

### 1. Clone repo and enter directory

git clone <your-repo-url>
cd spruce-greenops-vm-demo

---

### 2. Create Python environment (optional but recommended)

python3 -m venv venv
source venv/bin/activate

Install dependencies:

pip install pyspark requests pandas

---

### 3. Generate CUR dataset

python generate_cur.py

Expected output:
✔ CUR dataset written to: curs

Check output:

ls curs

---

### 4. Start VictoriaMetrics

docker run -d --name victoriametrics -p 8428:8428 victoriametrics/victoria-metrics

Verify:

http://localhost:8428/vmui

---

### 5. Push CUR metrics to VictoriaMetrics

pip install requests
python cur_to_victoriametrics.py

---

### 6. Validate ingestion in VMUI

Open:
http://localhost:8428/vmui

Query:

{__name__=~".*cost.*"}

Expected metrics:
- aws_cost_total
- aws_cost_service
- aws_cost_region
- aws_co2_estimate

---

### 7. Start Grafana

docker run -d --name grafana -p 3000:3000 grafana/grafana

Login:
http://localhost:3000
admin / admin

---

### 8. Add a Prometheus data source:

http://localhost:8428

---

### 9. Import dashboard:

grafana/dashboard.json

---

## 📈 Example Queries

### Total cost

sum(aws_cost_total)

### Cost by service

sum by (service) (aws_cost_service)

### CO₂ by region

sum by (region) (aws_co2_estimate)

### GreenOps efficiency score

sum(aws_cost_total) / sum(aws_co2_estimate)

---

## 📊 Suggested Grafana Dashboard

Panels:

- 💰 Total Cost (Stat)
- 🌍 Total CO₂ (Stat)
- 📈 Cost over time (Time series)
- 📈 CO₂ over time (Time series)
- ☁️ Cost by service (Bar chart)
- 🌍 CO₂ by region (Heatmap)
- ⚡ Efficiency score (Stat panel)

Below an example from my GreenOps CUR Dashboard

<img width="1689" height="817" alt="Screenshot 2026-06-25 at 10 07 49" src="https://github.com/user-attachments/assets/fdda7ce0-d409-424f-b26f-035f1ffbb735" />


---

## 🌍 Why this matters

Cloud sustainability is usually invisible.

This project shows that:

- Cost and carbon can be unified under observability
- Emissions can be derived from usage signals
- Infrastructure decisions can be made “green-aware”

---

## ⚡ Why VictoriaMetrics

- High-performance time-series engine
- Low resource usage (efficient footprint)
- PromQL compatible
- Ideal for cost + sustainability metrics

---

## 🧭 Future Work

- Real AWS CUR ingestion
- Kubernetes workload carbon tracking
- Carbon budgets per team/service
- Alerting on emission spikes
- Multi-cloud GreenOps comparison

---

## 📜 License

MIT
