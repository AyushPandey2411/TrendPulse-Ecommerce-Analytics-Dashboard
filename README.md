# 🛍️ TrendPulse: E-Commerce Analytics Dashboard

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live%20App-FF4B4B?style=flat&logo=streamlit&logoColor=white)](https://trendpulse-analytics.streamlit.app)
[![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?style=flat&logo=powerbi&logoColor=black)](https://github.com/AyushPandey2411/TrendPulse-Ecommerce-Analytics-Dashboard)
[![SQL](https://img.shields.io/badge/SQL-10%20Queries-336791?style=flat&logo=postgresql&logoColor=white)](./sql_queries.sql)
[![Prophet](https://img.shields.io/badge/Prophet-Forecasting-00A4EF?style=flat)](https://facebook.github.io/prophet/)

> **End-to-end E-Commerce Analytics Platform** — RFM Segmentation · Customer Lifetime Value · Cohort Retention · Sales Forecasting · SQL Analysis
>
> Built to mirror how BI & Analytics teams at Myntra, Flipkart, and Amazon use data to drive marketing, retention, and inventory decisions.

---

## 🚀 Live Demo

👉 **[Open Live Streamlit App](https://trendpulse-analytics.streamlit.app)**

---

## 📋 Project Overview

TrendPulse analyses **50,000+ e-commerce transactions (2023–2025)** across 8 product categories and 10 countries to deliver:

- 🎯 **RFM Customer Segmentation** — quintile-based scoring (industry standard)
- 💎 **Customer Lifetime Value** — 24-month CLV projection with tier classification
- 🔁 **Cohort Retention Analysis** — 18-cohort × 12-month heatmap
- 📈 **Revenue Trend Analysis** — MoM growth + 3-month rolling average
- 🔮 **Sales Forecasting** — Meta Prophet with 90% confidence intervals
- 🌍 **Geographic & Demographic Analysis** — country + age group breakdown
- 🗄️ **SQL Analysis** — 10 business queries with window functions and CTEs
- 📊 **Power BI Dashboard** — interactive executive KPI dashboard

---

## 🧰 Tech Stack

| Tool | Purpose |
|---|---|
| Python (Pandas, NumPy, Plotly) | Data processing & interactive visualisations |
| Prophet (Meta) | Time-series sales forecasting |
| Streamlit | 7-page interactive web application |
| SQL (SQLite) | Business query layer — 10 queries |
| Power BI | Executive KPI dashboard |
| Scikit-learn | CLV modelling & RFM scoring |

---

## 📁 Project Structure

```
TrendPulse-Ecommerce-Analytics-Dashboard/
│
├── 📓 TrendPulse_Analytics_Dashboard_UPGRADED.ipynb   ← Full analysis notebook
├── 🗄️ sql_queries.sql                                  ← 10 SQL business queries
├── 📊 business_analytics.pbix                          ← Power BI dashboard
├── 📋 requirements.txt
│
├── data/
│   └── ecommerce_transactions.csv                      ← 50K transactions
│
├── streamlit_app/                                       ← Live Streamlit app
│   ├── Home.py                                         ← KPIs + Revenue trend
│   ├── data_engine.py                                  ← Central analysis engine
│   └── pages/
│       ├── 1_Category_Intelligence.py
│       ├── 2_RFM_Segmentation.py
│       ├── 3_Customer_Lifetime_Value.py
│       ├── 4_Cohort_Retention.py
│       ├── 5_Geographic_Demographics.py
│       ├── 6_SQL_Analysis.py
│       └── 7_Sales_Forecast.py
│
└── .streamlit/
    └── config.toml                                     ← Dark theme config
```

---

## 📊 App Pages

| Page | Analysis | Key Output |
|---|---|---|
| 🏠 Home | KPIs + Revenue Trend | $25.1M revenue · 23.6% YoY growth |
| 📊 Category Intelligence | Revenue + Seasonal Heatmap | Sports leads at $3.2M (12.7%) |
| 🎯 RFM Segmentation | Quintile scoring + Action plan | 9 customer segments identified |
| 💎 Customer Lifetime Value | 24M CLV projection | $24.8M projected revenue |
| 🔁 Cohort Retention | 18-cohort heatmap | High repeat purchase behaviour |
| 🌍 Geographic & Demographics | Country + Age analysis | Even distribution across 10 markets |
| 🗄️ SQL Analysis | 10 live queries with syntax view | Window functions · CTEs · Subqueries |
| 🔮 Sales Forecast | Prophet · 90% CI | 6-month adjustable forecast horizon |

---

## 🔑 Key Findings

- **$25.1M total revenue** across 50,000 transactions with **23.6% YoY growth**
- **Sports** is the top revenue category at **$3.2M (12.7% share)**
- **56–70 age group** drives the highest revenue — through **frequency**, not higher AOV
- **Q4 seasonality confirmed** — recommend 15–20% inventory buffer for Electronics & Toys
- **Payment methods evenly split** (~17% each) — COD still popular, incentivise digital shift
- All **10 countries within 5%** of each other — strong global revenue diversification

---

## 🧩 SQL Concepts Demonstrated

| Query | Concept |
|---|---|
| Monthly Revenue + AOV | GROUP BY + Aggregates |
| Category % Contribution | `SUM() OVER()` Window Function |
| Top Customers by LTV | ORDER BY + LIMIT |
| Payment Method Analysis | Subquery |
| Country × Category Matrix | Multi-column GROUP BY |
| YoY Growth | CTE + Self Join |
| RFM Scoring | CTE + CASE WHEN |
| Cohort Retention | CTE + Date Functions |
| Age × Category Revenue | CASE WHEN Bucketing |
| 7-Day Rolling Average | `ROWS BETWEEN` Window Function |

---

## ⚙️ Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/AyushPandey2411/TrendPulse-Ecommerce-Analytics-Dashboard.git
cd TrendPulse-Ecommerce-Analytics-Dashboard

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run Streamlit app
streamlit run streamlit_app/Home.py

# 5. Or open the Jupyter notebook
jupyter notebook TrendPulse_Analytics_Dashboard_UPGRADED.ipynb
```

---

## 📸 Dashboard Preview

| Home — KPIs & Revenue Trend | RFM Segmentation |
|---|---|
| ![Home](https://via.placeholder.com/400x220/0a0a14/e94560?text=Home+Dashboard) | ![RFM](https://via.placeholder.com/400x220/0a0a14/e94560?text=RFM+Segmentation) |

| Cohort Retention Heatmap | Sales Forecast |
|---|---|
| ![Cohort](https://via.placeholder.com/400x220/0a0a14/e94560?text=Cohort+Retention) | ![Forecast](https://via.placeholder.com/400x220/0a0a14/e94560?text=Prophet+Forecast) |

> 💡 Replace placeholder images with actual screenshots after deployment

---

## 👤 Author

**Ayush Pandey**
[![GitHub](https://img.shields.io/badge/GitHub-AyushPandey2411-181717?style=flat&logo=github)](https://github.com/AyushPandey2411)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0077B5?style=flat&logo=linkedin)](https://linkedin.com/in/ayushpandey2411)

---

*Built as a Data Analyst / Business Analyst portfolio project — demonstrating end-to-end analytics from raw data to executive insights.*