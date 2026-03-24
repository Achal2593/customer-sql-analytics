# 🛒 Customer Purchase Behaviour — SQL Analytics

<div align="center">

![SQL](https://img.shields.io/badge/SQL-SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-11557c?style=for-the-badge&logo=python&logoColor=white)
![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-F37626?style=for-the-badge&logo=jupyter&logoColor=white)
![Status](https://img.shields.io/badge/Status-Completed-6bcb77?style=for-the-badge)

### Advanced SQL Analytics | 3-Table Database | 11 Queries | Window Functions | E-Commerce

</div>

---

## 🖼️ Dashboard Preview

![SQL Analytics Dashboard](sql_analytics_dashboard.png)

---

## 🎯 Objective

Analyze customer purchase behaviour for an electronics e-commerce company using a **3-table relational database** — identifying top customers, high-revenue categories, city-wise performance, and payment trends using **advanced SQL queries** including joins, subqueries, CASE WHEN, and window functions.

> 💡 This project demonstrates exact SQL skills tested in **Data Analyst interviews** at TCS, Infosys, Capgemini, Amazon, and Flipkart.

---

## 🗃️ Database Schema

```
┌─────────────┐       ┌─────────────┐       ┌─────────────┐
│  customers  │       │   orders    │       │  products   │
│─────────────│       │─────────────│       │─────────────│
│ customer_id │◄──────│ customer_id │──────►│ product_id  │
│ name, city  │       │ order_id    │       │ name, brand │
│ age, gender │       │ product_id  │       │ category    │
│ signup_date │       │ order_date  │       │ unit_price  │
│ cust_type   │       │ quantity    │       │ cost_price  │
└─────────────┘       │ discount_pct│       └─────────────┘
                      │ payment_mode│
                      └─────────────┘

Records: 30 customers | 20 products | 80 orders
```

---

## ❓ Business Questions Answered

| # | Business Question | SQL Technique |
|---|-----------------|---------------|
| 1 | Which category drives max revenue? | JOIN + GROUP BY + SUM |
| 2 | Who are top 10 customers by CLV? | 3-table JOIN + LIMIT |
| 3 | Which cities generate the most sales? | COUNT DISTINCT + GROUP BY |
| 4 | Monthly revenue trend? | SUBSTR date + GROUP BY |
| 5 | Most preferred payment mode? | COUNT + percentage calc |
| 6 | Do premium customers spend more? | GROUP BY customer_type |
| 7 | Top revenue products? | JOIN + ORDER BY + LIMIT |
| 8 | How often do customers return? | Subquery + CASE WHEN + Window |
| 9 | Which brand performs best? | JOIN + multi-aggregation |
| 10 | Cumulative revenue over time? | SUM() OVER (ORDER BY) |
| 11 | Orders above ₹50,000? | WHERE with expression |

---

## 📊 Key Results (KPIs)

| Metric | Value |
|--------|-------|
| 💰 Total Revenue | ₹ 25.2 Lakhs |
| 💵 Total Profit | ₹ 7.2 Lakhs |
| 📦 Total Orders | 80 |
| 👥 Total Customers | 30 |
| 🏙️ Top City | Delhi (₹6.55L) |
| 📱 Top Category | Laptops (₹8.48L) |
| 💳 Top Payment Mode | UPI (33.8%) |
| 🏆 Top Customer | Ritu Pandey (₹2.89L) |
| 🔁 Loyal Customers (4x+) | 40% |

---

## 🔍 SQL Highlights

```sql
-- Window Function: Cumulative Revenue (asked in interviews!)
SELECT
    SUBSTR(order_date, 1, 7) AS month,
    ROUND(SUM(o.quantity * p.unit_price * (1-o.discount_pct/100.0))/1000, 1) AS monthly_rev_K,
    ROUND(SUM(SUM(o.quantity * p.unit_price * (1-o.discount_pct/100.0)))
          OVER (ORDER BY SUBSTR(order_date,1,7))/1000, 1) AS cumulative_rev_K
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY month ORDER BY month;
```

```sql
-- 3-Table JOIN: Top 10 Customers by Revenue
SELECT c.customer_name, c.city, c.customer_type,
       COUNT(o.order_id) AS orders,
       ROUND(SUM(o.quantity * p.unit_price * (1-o.discount_pct/100.0))/1000,1) AS revenue_K
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p  ON o.product_id  = p.product_id
GROUP BY c.customer_id
ORDER BY revenue_K DESC LIMIT 10;
```

---

## 🛠️ SQL Concepts Covered

| Concept | Used In |
|---------|---------|
| ✅ INNER JOIN (2-table & 3-table) | Q1–Q11 |
| ✅ GROUP BY + ORDER BY | All queries |
| ✅ SUM, COUNT, AVG, ROUND | All queries |
| ✅ CASE WHEN (segmentation) | Q8 |
| ✅ Subqueries | Q8 |
| ✅ Window Functions: SUM OVER | Q10 |
| ✅ COUNT DISTINCT | Q3 |
| ✅ LIMIT (Top-N) | Q2, Q7, Q9 |
| ✅ SUBSTR for date extraction | Q4, Q10 |
| ✅ WHERE with expression | Bonus |
| ✅ Percentage calculation | Q5, Q8 |

---

## 📁 Project Structure

```
customer-sql-analytics/
│
├── 📓 SQL_Analytics.ipynb          ← Full notebook walkthrough
├── 🐍 analysis.py                  ← Python script version
├── 🗃️ customer_queries.sql         ← All 11 SQL queries with comments
├── 🖼️ sql_analytics_dashboard.png  ← 6-panel output dashboard
├── 📊 customers.csv                ← 30 customers
├── 📊 products.csv                 ← 20 products
├── 📊 orders.csv                   ← 80 orders
├── 📋 requirements.txt             ← Python dependencies
└── 📝 README.md
```

---

## 💡 Business Recommendations

| Priority | Recommendation | Based On |
|----------|---------------|----------|
| 🔴 HIGH | Promote EMI — only 1.3% usage | Payment analysis |
| 🔴 HIGH | Focus on Laptops + Mobiles (85% revenue) | Category analysis |
| 🟡 MED | Win-back campaign for 20% one-time buyers | Frequency analysis |
| 🟡 MED | Delhi + Mumbai = 48% revenue — target these | City analysis |
| 🟢 LOW | Premium customer loyalty program | Customer type |

---

## 🚀 How to Run

```bash
git clone https://github.com/Achal2593/customer-sql-analytics.git
cd customer-sql-analytics
pip install -r requirements.txt
python analysis.py
```

---

## 👤 About Me

**Achal Wakade** | Aspiring Data Analyst | Available immediately
🔗 [LinkedIn](https://linkedin.com/in/achal-wakade) | [GitHub](https://github.com/Achal2593)

---
<div align="center">⭐ If this helped you, please star the repo!</div>
