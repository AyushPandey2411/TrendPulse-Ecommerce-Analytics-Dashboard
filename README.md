# 🛍️ TrendPulse: E-Commerce Analytics Dashboard

**Data Analytics | Python | SQL | Power BI | RFM Segmentation | Forecasting | Customer Insights**

---

## 📊 Project Overview

**TrendPulse** is a full-scale **E-Commerce Sales & Customer Analytics Dashboard** designed to help retail businesses make smarter, data-driven decisions.

The project analyzes **50K+ sales transactions** to uncover:
- 🔝 Top-performing product categories & regions  
- 🎯 Key customer segments via **RFM analysis**  
- 💰 Profitability & retention patterns  
- 📈 Future sales forecasts with Prophet  

It mirrors how BI teams at **Myntra, Flipkart, or Amazon** use analytics for marketing & inventory optimization.

---

## 🧠 Business Objective

To uncover insights that drive:
- Targeted marketing & customer engagement  
- Improved retention through RFM segmentation  
- Smarter inventory planning (up to **20% efficiency boost**)  
- End-to-end KPI visibility across sales and customer data  

---

## 🧰 Tech Stack

| Tool | Purpose |
|------|----------|
| **Python (Pandas, NumPy, Matplotlib, Seaborn)** | Data cleaning, analysis & visualization |
| **Prophet (Meta)** | Time-series forecasting |
| **Power BI** | Interactive KPI dashboard & storytelling |
| **SQL** | Query-based data exploration |
| **Excel** | Quick data validation & pivot checks |

---

## 📂 Dataset

**Source:** Kaggle (E-commerce transactions dataset)  
**Records:** 50,000+  
**Time Period:** 2023–2024  

| Column | Description |
|--------|-------------|
| `Transaction_ID` | Unique order identifier |
| `User_Name` | Customer name |
| `Age` | Age of customer |
| `Country` | Customer location |
| `Product_Category` | Purchased product category |
| `Purchase_Amount` | Transaction value (USD) |
| `Payment_Method` | Mode of payment |
| `Transaction_Date` | Date of purchase |

---

## 🧩 Key Analyses

### 1️⃣ Sales & Revenue Trends  
- Monthly, regional, and category-wise sales analysis.  
- Identified top-performing regions & sales spikes.

### 2️⃣ Product & Country Performance  
- Highlighted top product categories using a **Tree Map**.  
- Country-based sales mapped for global visibility.

### 3️⃣ Customer Segmentation (RFM)  
Used **Recency, Frequency, Monetary (RFM)** model to identify:  
- 🥇 Champions  
- 💎 Loyal Customers  
- ⚠️ At Risk  
- ❌ Lost Customers  

### 4️⃣ Cohort Retention Analysis  
- Tracked repeat purchase behavior across months.  
- Evaluated long-term retention health.

### 5️⃣ Forecasting  
- Built **Prophet model** for future sales prediction.  
- Forecast visualized in Power BI.

---

## 📸 Power BI Dashboard Overview

All outputs from Python (CSV files) were loaded into **Power BI** for interactive visualization.

### 🎯 KPI Cards
| KPI | Formula | Purpose |
|------|----------|---------|
| **Total Sales** | `SUM(Purchase_Amount)` | Overall revenue |
| **Total Customers** | `DISTINCTCOUNT(User_Name)` | Unique buyers |
| **Average Order Value (AOV)** | `SUM(Purchase_Amount)/DISTINCTCOUNT(Transaction_ID)` | Avg. spend per order |

### 📊 Core Visuals
| Visual Type | Dataset | Insight |
|--------------|----------|----------|
| 📈 **Line Chart** | `monthly_sales.csv` | Sales trend over time |
| 🌳 **Tree Map** | `category_sales.csv` | Top-performing categories |
| 🌍 **Map Chart** | `country_sales.csv` | Regional performance |
| 💳 **Donut Chart** | `payment_sales.csv` | Payment method breakdown |
| 🧮 **Table / Heatmap** | `rfm_segments.csv` | Customer segmentation |
| 🔮 **Forecast Line** | Prophet Output | Future sales projection |

---

## 🖼️ Power BI Layout Suggestion

**Dashboard Sections:**


## 📸 Visual Insights
<img width="1492" height="717" alt="image" src="https://github.com/user-attachments/assets/608f5519-6569-463a-9647-157cbfb28eb3" />

<img width="1307" height="662" alt="image" src="https://github.com/user-attachments/assets/00910ed6-8b79-4c4b-8dac-027b2f07af76" />
<img width="1919" height="982" alt="image" src="https://github.com/user-attachments/assets/8338c95d-ea0f-4935-a50d-cd0e09303e3d" />








