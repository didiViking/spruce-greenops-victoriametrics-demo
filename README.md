# 🌱 GreenOps Observability Demo (CUR → VictoriaMetrics → Grafana)

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-demo-orange.svg)
![Stack](https://img.shields.io/badge/stack-spark%20%7C%20victoriametrics%20%7C%20grafana-green.svg)

A GreenOps observability pipeline that transforms AWS Cost and Usage Report (CUR)-like data into cost and carbon metrics, then visualizes them using **VictoriaMetrics + Grafana**.

This project demonstrates how sustainability can be treated as a **first-class observability signal**.

This project demo is inspired by the OSS Spruce project: https://github.com/digitalpebble/spruce

---

## ✨ Key Ideas

- Treat cloud cost as a metric
- Derive carbon emissions from usage data
- Use observability tooling for sustainability insights
- Keep the stack lightweight and reproducible

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

### 1. Generate CUR dataset

python generate_cur.py

Output:
curs/

---

### 2. Export metrics to VictoriaMetrics

python cur_to_victoriametrics.py

Push endpoint:
http://localhost:8428

---

### 3. Start VictoriaMetrics

docker run -p 8428:8428 victoriametrics/victoria-metrics

---

### 4. Start Grafana

Add a Prometheus data source:

http://localhost:8428

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
