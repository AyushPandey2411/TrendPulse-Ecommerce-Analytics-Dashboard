# 🛍️ TrendPulse: E-Commerce Analytics Dashboard

**Stack:** Python · SQL (SQLite) · Prophet · Power BI  
**Dataset:** 50,000+ transactions · 2023–2025  
**Target Roles:** Data Analyst · Business Analyst

## 📁 Project Structure
```
TrendPulse/
├── TrendPulse_Analytics_Dashboard_UPGRADED.ipynb   ← Main notebook (run this)
├── ecommerce_transactions.csv                       ← Raw dataset
├── requirements.txt                                 ← Python dependencies
└── exports/                                         ← All outputs for Power BI
    ├── 01_revenue_trend.png
    ├── 02_category_analysis.png
    ├── 03_rfm_segmentation.png
    ├── 04_customer_clv.png
    ├── 05_cohort_retention.png
    ├── 06_geo_demographic.png
    ├── 07_payment_behaviour.png
    ├── monthly_sales.csv
    ├── category_sales.csv
    ├── country_sales.csv
    ├── payment_sales.csv
    ├── rfm_segments.csv
    ├── customer_clv.csv
    ├── cohort_retention.csv
    ├── sales_forecast.csv
    ├── kpi_summary.csv
    └── business_insights.txt
```

## 🚀 Setup & Run
```bash
pip install -r requirements.txt
jupyter notebook TrendPulse_Analytics_Dashboard_UPGRADED.ipynb
```

## 📊 Analyses Included
| Analysis | Technique | Business Value |
|---|---|---|
| Revenue Trend | MoM % + Rolling Avg | Growth tracking |
| Category Intelligence | Revenue + Seasonal Heatmap | Inventory planning |
| RFM Segmentation | Quintile scoring | Targeted marketing |
| Customer Lifetime Value | AOV × Freq × 24M | Retention ROI |
| Cohort Retention | 18-cohort heatmap | Churn detection |
| Geographic Analysis | Country + Age cross-tab | Market expansion |
| Sales Forecast | Prophet (90% CI) | Budget planning |
| SQL Analysis | 5 business queries | BI/DA skill demo |

## 💡 Key Findings
- **$25.1M total revenue** across 50,000 transactions
- **+23.6% YoY growth** (2023 → 2024)
- **Sports** is the top revenue category at $3.2M (12.7%)
- **56–70 age group** drives most revenue via higher purchase frequency
- **Q4 seasonality confirmed** — plan 15–20% inventory buffer
