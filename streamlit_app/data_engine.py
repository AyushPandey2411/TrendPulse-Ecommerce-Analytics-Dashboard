"""
data_engine.py
──────────────
Central analysis engine — loads raw CSV and computes all metrics live.
Cached with @st.cache_data so analysis only runs once per session.
"""

import pandas as pd
import numpy as np
import os, sys

# ── Path resolution ───────────────────────────────────────────────────────────
APP_DIR  = os.path.dirname(os.path.abspath(__file__))
ROOT     = os.path.dirname(APP_DIR)
DATA_DIR = os.path.join(ROOT, "data")

DATA_PATH = os.path.join(DATA_DIR, "ecommerce_transactions.csv")

import streamlit as st

# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def load_and_process():
    """Load raw CSV and return all computed DataFrames."""

    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df = df.dropna().drop_duplicates().sort_values("transaction_date").reset_index(drop=True)

    # Derived columns
    df["year"]        = df["transaction_date"].dt.year
    df["month"]       = df["transaction_date"].dt.month
    df["quarter"]     = df["transaction_date"].dt.quarter
    df["day_of_week"] = df["transaction_date"].dt.day_name()
    df["order_month"] = df["transaction_date"].dt.to_period("M")
    df["age_group"]   = pd.cut(df["age"], bins=[17,25,35,45,55,70],
                                labels=["18–25","26–35","36–45","46–55","56–70"])

    return df


@st.cache_data
def get_kpis():
    df = load_and_process()
    total_revenue    = df["purchase_amount"].sum()
    total_orders     = df["transaction_id"].nunique()
    unique_customers = df["user_name"].nunique()
    aov              = total_revenue / total_orders
    avg_orders_cust  = total_orders / unique_customers
    rev_2023 = df[df["year"]==2023]["purchase_amount"].sum()
    rev_2024 = df[df["year"]==2024]["purchase_amount"].sum()
    yoy = ((rev_2024 - rev_2023) / rev_2023) * 100
    return {
        "total_revenue":    total_revenue,
        "total_orders":     total_orders,
        "unique_customers": unique_customers,
        "aov":              aov,
        "avg_orders_cust":  avg_orders_cust,
        "yoy_growth":       yoy,
        "rev_2023":         rev_2023,
        "rev_2024":         rev_2024,
    }


@st.cache_data
def get_monthly():
    df = load_and_process()
    monthly = df.groupby("order_month").agg(
        revenue  =("purchase_amount","sum"),
        orders   =("transaction_id","count"),
        customers=("user_name","nunique")
    ).reset_index()
    monthly["order_month_str"] = monthly["order_month"].astype(str)
    monthly["mom_growth"]      = monthly["revenue"].pct_change() * 100
    monthly["rolling_3m"]      = monthly["revenue"].rolling(3).mean()
    return monthly


@st.cache_data
def get_category_stats():
    df = load_and_process()
    cat = df.groupby("product_category").agg(
        revenue  =("purchase_amount","sum"),
        orders   =("transaction_id","count"),
        customers=("user_name","nunique"),
        avg_order=("purchase_amount","mean")
    ).reset_index().sort_values("revenue", ascending=False)
    cat["revenue_pct"] = cat["revenue"] / cat["revenue"].sum() * 100
    cat_quarter = df.groupby(["product_category","quarter"])["purchase_amount"].sum().unstack()
    return cat, cat_quarter


@st.cache_data
def get_rfm():
    df = load_and_process()
    snapshot = df["transaction_date"].max() + pd.Timedelta(days=1)
    rfm = df.groupby("user_name").agg(
        recency  =("transaction_date", lambda x: (snapshot - x.max()).days),
        frequency=("transaction_id","count"),
        monetary =("purchase_amount","sum")
    ).reset_index()

    rfm["r_score"] = pd.cut(rfm["recency"].rank(method="first", ascending=False),
                             5, labels=[5,4,3,2,1]).astype(int)
    rfm["f_score"] = pd.cut(rfm["frequency"].rank(method="first"),
                             5, labels=[1,2,3,4,5]).astype(int)
    rfm["m_score"] = pd.cut(rfm["monetary"].rank(method="first"),
                             5, labels=[1,2,3,4,5]).astype(int)
    rfm["rfm_score"] = rfm["r_score"] + rfm["f_score"] + rfm["m_score"]

    def segment(row):
        r, f, m, t = row["r_score"], row["f_score"], row["m_score"], row["rfm_score"]
        if r>=4 and f>=4 and m>=4:    return "Champions"
        elif r>=3 and f>=3 and m>=3:  return "Loyal Customers"
        elif r>=4 and f<=2:           return "New Customers"
        elif r>=3 and t>=9:           return "Potential Loyalists"
        elif r==3 and f>=3:           return "Needs Attention"
        elif r<=2 and f>=3 and m>=3:  return "At Risk"
        elif r<=2 and t>=8:           return "Cannot Lose Them"
        elif r<=2 and t<=6:           return "Lost Customers"
        else:                          return "Hibernating"

    rfm["segment"] = rfm.apply(segment, axis=1)

    seg_summary = rfm.groupby("segment").agg(
        customers    =("user_name","count"),
        avg_recency  =("recency","mean"),
        avg_frequency=("frequency","mean"),
        avg_monetary =("monetary","mean"),
        total_revenue=("monetary","sum")
    ).reset_index()
    seg_summary["revenue_pct"] = (seg_summary["total_revenue"] /
                                  seg_summary["total_revenue"].sum() * 100)
    return rfm, seg_summary.sort_values("total_revenue", ascending=False)


@st.cache_data
def get_clv():
    df = load_and_process()
    cs = df.groupby("user_name").agg(
        total_spend   =("purchase_amount","sum"),
        orders        =("transaction_id","count"),
        first_purchase=("transaction_date","min"),
        last_purchase =("transaction_date","max"),
    ).reset_index()
    cs["tenure_days"]    = (cs["last_purchase"] - cs["first_purchase"]).dt.days.clip(lower=1)
    cs["avg_order_value"] = cs["total_spend"] / cs["orders"]
    cs["purchase_freq"]   = cs["orders"] / (cs["tenure_days"] / 30)
    cs["clv_24m"]         = (cs["avg_order_value"] * cs["purchase_freq"] * 24).round(2)
    cs["clv_tier"] = pd.qcut(cs["clv_24m"], q=4,
                              labels=["Low Value","Medium Value","High Value","Premium"])
    tier_summary = cs.groupby("clv_tier", observed=True).agg(
        customers           =("user_name","count"),
        avg_clv             =("clv_24m","mean"),
        total_projected_rev =("clv_24m","sum")
    ).reset_index()
    return cs, tier_summary


@st.cache_data
def get_cohort():
    df = load_and_process()
    df = df.copy()
    df["first_purchase_month"] = (df.groupby("user_name")["transaction_date"]
                                   .transform("min").dt.to_period("M"))
    df["cohort_index"] = (df["order_month"] - df["first_purchase_month"]).apply(lambda x: x.n)
    cohort_data = (df.groupby(["first_purchase_month","cohort_index"])["user_name"]
                   .nunique().reset_index())
    pivot        = cohort_data.pivot(index="first_purchase_month",
                                     columns="cohort_index", values="user_name")
    sizes        = pivot[0]
    retention    = pivot.divide(sizes, axis=0).round(3) * 100
    return retention


@st.cache_data
def get_geo():
    df = load_and_process()
    country = df.groupby("country").agg(
        revenue  =("purchase_amount","sum"),
        orders   =("transaction_id","count"),
        customers=("user_name","nunique"),
        avg_order=("purchase_amount","mean")
    ).reset_index().sort_values("revenue", ascending=False)
    country["revenue_pct"] = country["revenue"] / country["revenue"].sum() * 100

    age = df.groupby("age_group", observed=True).agg(
        revenue  =("purchase_amount","sum"),
        orders   =("transaction_id","count"),
        avg_order=("purchase_amount","mean")
    ).reset_index()

    payment = df.groupby("payment_method").agg(
        revenue  =("purchase_amount","sum"),
        orders   =("transaction_id","count"),
        avg_order=("purchase_amount","mean")
    ).reset_index().sort_values("revenue", ascending=False)
    payment["txn_pct"] = payment["orders"] / payment["orders"].sum() * 100

    dow_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    dow = (df.groupby("day_of_week")["purchase_amount"]
           .agg(["sum","count","mean"]).reindex(dow_order))

    return country, age, payment, dow
