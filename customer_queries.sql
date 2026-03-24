-- ============================================================
--  PROJECT: Customer Purchase Behaviour — SQL Analytics
--  Author : Achal Wakade
--  Tool   : SQLite / PostgreSQL compatible
--  Tables : customers, products, orders
-- ============================================================
--
--  DATABASE SCHEMA:
--  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
--  │  customers  │     │   orders    │     │  products   │
--  │─────────────│     │─────────────│     │─────────────│
--  │ customer_id │◄────│ customer_id │────►│ product_id  │
--  │ name, city  │     │ order_id    │     │ name, brand │
--  │ age, gender │     │ product_id  │     │ category    │
--  │ signup_date │     │ order_date  │     │ unit_price  │
--  │ cust_type   │     │ quantity    │     │ cost_price  │
--  └─────────────┘     │ discount_pct│     └─────────────┘
--                      │ payment_mode│
--                      └─────────────┘
-- ============================================================


-- ── QUERY 1: Revenue & Profit by Category ────────────────────
-- Business Question: Which product category drives the most revenue?
-- SQL Concepts: JOIN, GROUP BY, SUM, ROUND, arithmetic expressions

SELECT
    p.category,
    COUNT(o.order_id)                                                          AS total_orders,
    SUM(o.quantity)                                                            AS units_sold,
    ROUND(SUM(o.quantity * p.unit_price * (1-o.discount_pct/100.0))/1000, 1) AS revenue_K,
    ROUND(SUM(o.quantity * (p.unit_price*(1-o.discount_pct/100.0)
              - p.cost_price))/1000, 1)                                        AS profit_K,
    ROUND(AVG(o.discount_pct), 1)                                              AS avg_discount
FROM   orders o
JOIN   products p ON o.product_id = p.product_id
GROUP  BY p.category
ORDER  BY revenue_K DESC;

/*
Key Finding: Laptops = top revenue category (₹848K)
             Followed by Mobiles (₹790K)
*/


-- ── QUERY 2: Customer Lifetime Value (Top 10) ────────────────
-- Business Question: Who are our highest-value customers?
-- SQL Concepts: 3-table JOIN, GROUP BY, AVG, LIMIT

SELECT
    c.customer_name,
    c.city,
    c.customer_type,
    COUNT(o.order_id)                                                          AS total_orders,
    ROUND(SUM(o.quantity * p.unit_price * (1-o.discount_pct/100.0))/1000, 1) AS revenue_K,
    ROUND(AVG(o.quantity * p.unit_price * (1-o.discount_pct/100.0))/1000, 2) AS avg_order_K
FROM   orders o
JOIN   customers c ON o.customer_id = c.customer_id
JOIN   products p  ON o.product_id  = p.product_id
GROUP  BY c.customer_id
ORDER  BY revenue_K DESC
LIMIT  10;

/*
Key Finding: Top customer = Ritu Pandey (₹289K)
             Premium customers have higher avg order value
*/


-- ── QUERY 3: City-wise Sales Performance ─────────────────────
-- Business Question: Which cities generate the most revenue?
-- SQL Concepts: JOIN, GROUP BY, COUNT DISTINCT, ORDER BY

SELECT
    c.city,
    c.state,
    COUNT(DISTINCT c.customer_id)                                              AS unique_customers,
    COUNT(o.order_id)                                                          AS total_orders,
    ROUND(SUM(o.quantity * p.unit_price * (1-o.discount_pct/100.0))/1000, 1) AS revenue_K
FROM   orders o
JOIN   customers c ON o.customer_id = c.customer_id
JOIN   products p  ON o.product_id  = p.product_id
GROUP  BY c.city
ORDER  BY revenue_K DESC;

/*
Key Finding: Delhi leads (₹655K), followed by Mumbai (₹577K)
             Ahmedabad has fewest customers but decent revenue per order
*/


-- ── QUERY 4: Monthly Revenue Trend ───────────────────────────
-- Business Question: How does revenue grow month over month?
-- SQL Concepts: SUBSTR for date extraction, GROUP BY, ORDER BY

SELECT
    SUBSTR(o.order_date, 1, 7)                                                AS month,
    COUNT(o.order_id)                                                          AS orders,
    ROUND(SUM(o.quantity * p.unit_price * (1-o.discount_pct/100.0))/1000, 1) AS revenue_K
FROM   orders o
JOIN   products p ON o.product_id = p.product_id
GROUP  BY month
ORDER  BY month;


-- ── QUERY 5: Payment Mode Analysis ───────────────────────────
-- Business Question: Which payment mode is most preferred?
-- SQL Concepts: GROUP BY, COUNT, percentage calculation

SELECT
    payment_mode,
    COUNT(*)                                                                   AS transactions,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM orders), 1)                AS pct_share,
    ROUND(SUM(o.quantity * p.unit_price * (1-o.discount_pct/100.0))/1000, 1) AS revenue_K
FROM   orders o
JOIN   products p ON o.product_id = p.product_id
GROUP  BY payment_mode
ORDER  BY transactions DESC;

/*
Key Finding: UPI is the top mode (33.8%)
             EMI is least used (1.3%) — opportunity to promote
*/


-- ── QUERY 6: Premium vs Regular Customer Comparison ──────────
-- Business Question: Do premium customers spend more?
-- SQL Concepts: JOIN, GROUP BY on derived attribute, AVG

SELECT
    c.customer_type,
    COUNT(DISTINCT c.customer_id)                                              AS customers,
    COUNT(o.order_id)                                                          AS total_orders,
    ROUND(SUM(o.quantity * p.unit_price * (1-o.discount_pct/100.0))/1000, 1) AS total_revenue_K,
    ROUND(AVG(o.quantity * p.unit_price * (1-o.discount_pct/100.0))/1000, 2) AS avg_order_value_K
FROM   orders o
JOIN   customers c ON o.customer_id = c.customer_id
JOIN   products p  ON o.product_id  = p.product_id
GROUP  BY c.customer_type;

/*
Key Finding: Premium customers have higher avg order value
             Target for upsell and loyalty programs
*/


-- ── QUERY 7: Top 5 Products by Revenue ───────────────────────
-- Business Question: Which individual products sell the most?
-- SQL Concepts: JOIN, GROUP BY, ORDER BY, LIMIT

SELECT
    p.product_name,
    p.category,
    p.brand,
    SUM(o.quantity)                                                            AS units_sold,
    ROUND(SUM(o.quantity * p.unit_price * (1-o.discount_pct/100.0))/1000, 1) AS revenue_K,
    ROUND(SUM(o.quantity * (p.unit_price*(1-o.discount_pct/100.0) - p.cost_price))/1000,1) AS profit_K
FROM   orders o
JOIN   products p ON o.product_id = p.product_id
GROUP  BY p.product_id
ORDER  BY revenue_K DESC
LIMIT  5;


-- ── QUERY 8: Customer Purchase Frequency (Window Function) ───
-- Business Question: How often do customers come back?
-- SQL Concepts: Subquery, CASE WHEN, Window Function (SUM OVER)

SELECT
    purchase_freq,
    COUNT(*)                                                   AS customers,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1)        AS pct
FROM (
    SELECT
        customer_id,
        CASE
            WHEN COUNT(order_id) = 1            THEN 'One-time'
            WHEN COUNT(order_id) BETWEEN 2 AND 3 THEN 'Occasional (2-3x)'
            ELSE                                     'Loyal (4x+)'
        END AS purchase_freq
    FROM   orders
    GROUP  BY customer_id
) sub
GROUP  BY purchase_freq
ORDER  BY customers DESC;

/*
Key Finding: 40% customers are Loyal (4x+ purchases)
             20% are One-time — target for win-back campaigns
*/


-- ── QUERY 9: Brand Performance ───────────────────────────────
-- Business Question: Which brands drive the most revenue?
-- SQL Concepts: JOIN, GROUP BY, multiple aggregations

SELECT
    p.brand,
    COUNT(o.order_id)                                                          AS orders,
    SUM(o.quantity)                                                            AS units_sold,
    ROUND(SUM(o.quantity * p.unit_price * (1-o.discount_pct/100.0))/1000, 1) AS revenue_K,
    ROUND(AVG(o.discount_pct), 1)                                              AS avg_discount_pct
FROM   orders o
JOIN   products p ON o.product_id = p.product_id
GROUP  BY p.brand
ORDER  BY revenue_K DESC
LIMIT  10;


-- ── QUERY 10: Cumulative Revenue (Running Total) ─────────────
-- Business Question: What is the running total of revenue over time?
-- SQL Concepts: Window Function — SUM() OVER (ORDER BY), GROUP BY

SELECT
    SUBSTR(order_date, 1, 7)                                                  AS month,
    ROUND(SUM(o.quantity * p.unit_price*(1-o.discount_pct/100.0))/1000, 1)  AS monthly_rev_K,
    ROUND(SUM(SUM(o.quantity * p.unit_price*(1-o.discount_pct/100.0)))
          OVER (ORDER BY SUBSTR(order_date,1,7)) / 1000, 1)                  AS cumulative_rev_K
FROM   orders o
JOIN   products p ON o.product_id = p.product_id
GROUP  BY month
ORDER  BY month;

/*
Window function breakdown:
  - Inner SUM() → aggregates revenue per month
  - Outer SUM() OVER (ORDER BY month) → running total across months
This is a common Data Analyst interview question!
*/


-- ── BONUS QUERY: High-Value Order Filter ─────────────────────
-- Business Question: Which orders were above ₹50,000?
-- SQL Concepts: WHERE with calculated expression, JOIN

SELECT
    o.order_id,
    o.order_date,
    c.customer_name,
    c.city,
    p.product_name,
    p.category,
    o.quantity,
    ROUND(o.quantity * p.unit_price * (1-o.discount_pct/100.0), 0) AS order_value
FROM   orders o
JOIN   customers c ON o.customer_id = c.customer_id
JOIN   products p  ON o.product_id  = p.product_id
WHERE  (o.quantity * p.unit_price * (1-o.discount_pct/100.0)) > 50000
ORDER  BY order_value DESC;


-- ============================================================
--  SQL CONCEPTS USED IN THIS PROJECT:
--  ✅ INNER JOIN (2-table and 3-table)
--  ✅ GROUP BY + ORDER BY
--  ✅ SUM, COUNT, AVG, ROUND
--  ✅ Arithmetic in SELECT (revenue, profit calculation)
--  ✅ CASE WHEN (customer segmentation)
--  ✅ Subqueries (nested SELECT)
--  ✅ Window Functions: SUM() OVER (ORDER BY)
--  ✅ COUNT DISTINCT
--  ✅ LIMIT (top N records)
--  ✅ SUBSTR (date extraction)
--  ✅ Percentage calculation
--  ✅ WHERE with expression filter
-- ============================================================
