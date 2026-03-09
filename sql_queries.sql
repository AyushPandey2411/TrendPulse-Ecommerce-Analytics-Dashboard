-- ============================================================
-- TrendPulse: E-Commerce Analytics — SQL Query Bank
-- Author  : Ayush Pandey
-- Stack   : SQLite / compatible with PostgreSQL & MySQL
-- Dataset : 50,000 e-commerce transactions (2023–2025)
-- ============================================================


-- ============================================================
-- QUERY 1: Monthly Revenue, Orders & Average Order Value
-- Concept : GROUP BY + Aggregate functions
-- Use case: Track revenue trend month over month
-- ============================================================

SELECT
    order_month,
    ROUND(SUM(purchase_amount), 2)                                    AS revenue,
    COUNT(DISTINCT transaction_id)                                     AS total_orders,
    COUNT(DISTINCT user_name)                                          AS unique_customers,
    ROUND(SUM(purchase_amount) / COUNT(DISTINCT transaction_id), 2)   AS avg_order_value
FROM transactions
GROUP BY order_month
ORDER BY order_month;


-- ============================================================
-- QUERY 2: Category Revenue with % Contribution
-- Concept : Window function — SUM() OVER()
-- Use case: Identify top-performing categories and their share
-- ============================================================

SELECT
    product_category,
    ROUND(SUM(purchase_amount), 2)                                     AS revenue,
    COUNT(DISTINCT transaction_id)                                      AS total_orders,
    ROUND(AVG(purchase_amount), 2)                                      AS avg_order_value,
    ROUND(
        100.0 * SUM(purchase_amount) /
        SUM(SUM(purchase_amount)) OVER (), 2
    )                                                                   AS revenue_pct
FROM transactions
GROUP BY product_category
ORDER BY revenue DESC;


-- ============================================================
-- QUERY 3: Top 20 Customers by Lifetime Value
-- Concept : GROUP BY + ORDER BY + LIMIT
-- Use case: Identify VIP customers for loyalty programme
-- ============================================================

SELECT
    user_name,
    COUNT(DISTINCT transaction_id)          AS total_orders,
    ROUND(SUM(purchase_amount), 2)          AS lifetime_spend,
    ROUND(AVG(purchase_amount), 2)          AS avg_order_value,
    MIN(transaction_date)                   AS first_purchase,
    MAX(transaction_date)                   AS last_purchase,
    ROUND(
        julianday(MAX(transaction_date)) -
        julianday(MIN(transaction_date))
    )                                       AS tenure_days
FROM transactions
GROUP BY user_name
ORDER BY lifetime_spend DESC
LIMIT 20;


-- ============================================================
-- QUERY 4: Payment Method Revenue & Transaction Share
-- Concept : Subquery for denominator
-- Use case: Understand payment preferences and AOV by method
-- ============================================================

SELECT
    payment_method,
    COUNT(*)                                                            AS total_transactions,
    ROUND(SUM(purchase_amount), 2)                                      AS revenue,
    ROUND(AVG(purchase_amount), 2)                                      AS avg_order_value,
    ROUND(
        100.0 * COUNT(*) /
        (SELECT COUNT(*) FROM transactions), 2
    )                                                                   AS txn_share_pct
FROM transactions
GROUP BY payment_method
ORDER BY revenue DESC;


-- ============================================================
-- QUERY 5: Country × Category Revenue Cross-Tab
-- Concept : Multi-column GROUP BY
-- Use case: Find market-specific category opportunities
-- ============================================================

SELECT
    country,
    product_category,
    ROUND(SUM(purchase_amount), 2)          AS revenue,
    COUNT(*)                                AS total_orders,
    ROUND(AVG(purchase_amount), 2)          AS avg_order_value
FROM transactions
GROUP BY country, product_category
ORDER BY country, revenue DESC;


-- ============================================================
-- QUERY 6: Year-over-Year Revenue Growth
-- Concept : CTE + self-join for YoY comparison
-- Use case: Executive summary — is the business growing?
-- ============================================================

WITH yearly AS (
    SELECT
        strftime('%Y', transaction_date)    AS year,
        ROUND(SUM(purchase_amount), 2)      AS revenue
    FROM transactions
    GROUP BY year
)
SELECT
    curr.year,
    curr.revenue                            AS current_revenue,
    prev.revenue                            AS previous_revenue,
    ROUND(
        100.0 * (curr.revenue - prev.revenue) / prev.revenue, 2
    )                                       AS yoy_growth_pct
FROM yearly curr
LEFT JOIN yearly prev
    ON CAST(curr.year AS INTEGER) = CAST(prev.year AS INTEGER) + 1
ORDER BY curr.year;


-- ============================================================
-- QUERY 7: RFM Scoring — Recency, Frequency, Monetary
-- Concept : CTE + CASE WHEN + date functions
-- Use case: Customer segmentation for targeted marketing
-- ============================================================

WITH rfm_base AS (
    SELECT
        user_name,
        ROUND(julianday('now') - julianday(MAX(transaction_date)))  AS recency_days,
        COUNT(DISTINCT transaction_id)                               AS frequency,
        ROUND(SUM(purchase_amount), 2)                              AS monetary
    FROM transactions
    GROUP BY user_name
),
rfm_scored AS (
    SELECT
        user_name,
        recency_days,
        frequency,
        monetary,
        CASE
            WHEN recency_days <= 30  THEN 5
            WHEN recency_days <= 60  THEN 4
            WHEN recency_days <= 90  THEN 3
            WHEN recency_days <= 180 THEN 2
            ELSE 1
        END AS r_score,
        CASE
            WHEN frequency >= 500 THEN 5
            WHEN frequency >= 450 THEN 4
            WHEN frequency >= 400 THEN 3
            WHEN frequency >= 350 THEN 2
            ELSE 1
        END AS f_score,
        CASE
            WHEN monetary >= 250000 THEN 5
            WHEN monetary >= 220000 THEN 4
            WHEN monetary >= 190000 THEN 3
            WHEN monetary >= 160000 THEN 2
            ELSE 1
        END AS m_score
    FROM rfm_base
)
SELECT
    user_name,
    recency_days,
    frequency,
    monetary,
    r_score,
    f_score,
    m_score,
    (r_score + f_score + m_score)   AS rfm_total,
    CASE
        WHEN (r_score + f_score + m_score) >= 13 THEN 'Champions'
        WHEN (r_score + f_score + m_score) >= 10 THEN 'Loyal Customers'
        WHEN (r_score + f_score + m_score) >= 7  THEN 'At Risk'
        ELSE 'Lost Customers'
    END                             AS segment
FROM rfm_scored
ORDER BY rfm_total DESC;


-- ============================================================
-- QUERY 8: Cohort Retention — First Purchase Month
-- Concept : CTE + date truncation + self-join
-- Use case: Track repeat purchase behaviour over time
-- ============================================================

WITH first_purchase AS (
    SELECT
        user_name,
        MIN(strftime('%Y-%m', transaction_date))    AS cohort_month
    FROM transactions
    GROUP BY user_name
),
cohort_data AS (
    SELECT
        f.cohort_month,
        strftime('%Y-%m', t.transaction_date)       AS order_month,
        COUNT(DISTINCT t.user_name)                  AS customers
    FROM transactions t
    JOIN first_purchase f ON t.user_name = f.user_name
    GROUP BY f.cohort_month, order_month
)
SELECT
    cohort_month,
    order_month,
    customers
FROM cohort_data
ORDER BY cohort_month, order_month;


-- ============================================================
-- QUERY 9: Revenue by Age Group and Category
-- Concept : CASE WHEN bucketing + multi-dimension GROUP BY
-- Use case: Demographic targeting for category promotions
-- ============================================================

SELECT
    CASE
        WHEN age BETWEEN 18 AND 25 THEN '18-25'
        WHEN age BETWEEN 26 AND 35 THEN '26-35'
        WHEN age BETWEEN 36 AND 45 THEN '36-45'
        WHEN age BETWEEN 46 AND 55 THEN '46-55'
        WHEN age BETWEEN 56 AND 70 THEN '56-70'
    END                                             AS age_group,
    product_category,
    ROUND(SUM(purchase_amount), 2)                  AS revenue,
    COUNT(*)                                        AS orders,
    ROUND(AVG(purchase_amount), 2)                  AS avg_order_value
FROM transactions
GROUP BY age_group, product_category
ORDER BY age_group, revenue DESC;


-- ============================================================
-- QUERY 10: 7-Day Rolling Revenue (Moving Average)
-- Concept : Window function with ROWS BETWEEN
-- Use case: Smooth daily revenue fluctuations for trend view
-- ============================================================

WITH daily AS (
    SELECT
        DATE(transaction_date)              AS sale_date,
        ROUND(SUM(purchase_amount), 2)      AS daily_revenue
    FROM transactions
    GROUP BY sale_date
)
SELECT
    sale_date,
    daily_revenue,
    ROUND(
        AVG(daily_revenue) OVER (
            ORDER BY sale_date
            ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
        ), 2
    )                                       AS rolling_7d_avg
FROM daily
ORDER BY sale_date;
