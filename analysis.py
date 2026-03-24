# ============================================================
#  PROJECT 3: Customer Purchase Behaviour — SQL Analytics
#  Author : Achal Wakade
#  Tools  : Python | Pandas | SQLite | Matplotlib
#  GitHub : github.com/Achal2593/customer-sql-analytics
# ============================================================
#
#  WHAT THIS PROJECT DOES:
#  ─────────────────────────────────────────────────────────
#  1. Creates a realistic e-commerce database (3 tables)
#  2. Runs 10 advanced SQL queries
#  3. Prints all query results in terminal
#  4. Produces a professional 6-panel dashboard PNG
#  5. Saves dataset as CSV
#
#  HOW TO RUN:
#  pip install pandas numpy matplotlib
#  python analysis.py
#
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import sqlite3
import warnings
warnings.filterwarnings('ignore')

# ════════════════════════════════════════════════════════════
#  STYLE
# ════════════════════════════════════════════════════════════
BG_DARK  = '#0a0a14'
BG_PANEL = '#12121e'
TEXT_C   = '#e8e8f0'
SUB_C    = '#8888aa'
GRID_C   = '#1e1e30'
ACCENT   = ['#00d4ff','#ff6b6b','#ffd93d','#6bcb77','#c77dff','#ff9f43']

plt.rcParams.update({
    'figure.facecolor':BG_DARK,'axes.facecolor':BG_PANEL,
    'axes.edgecolor':'#1e1e30','axes.labelcolor':SUB_C,
    'axes.labelsize':10,'axes.titlesize':12,'axes.titlecolor':TEXT_C,
    'axes.titleweight':'bold','xtick.color':SUB_C,'ytick.color':SUB_C,
    'xtick.labelsize':9,'ytick.labelsize':9,'text.color':TEXT_C,
    'grid.color':GRID_C,'grid.linestyle':'--','grid.alpha':0.6,
    'legend.facecolor':BG_PANEL,'legend.edgecolor':'#1e1e30',
    'legend.labelcolor':TEXT_C,'font.family':'monospace',
})

# ════════════════════════════════════════════════════════════
#  SECTION 1 — DATABASE SETUP (3 Tables)
# ════════════════════════════════════════════════════════════
print("="*60)
print("  🛒 CUSTOMER PURCHASE BEHAVIOUR — SQL ANALYTICS")
print("="*60)
print("\n[1/5] Setting up database...")

conn = sqlite3.connect(':memory:')
cur  = conn.cursor()

# ── Create Tables ─────────────────────────────────────────
cur.executescript("""
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS orders;

CREATE TABLE customers (
    customer_id    INTEGER PRIMARY KEY,
    customer_name  TEXT,
    city           TEXT,
    state          TEXT,
    age            INTEGER,
    gender         TEXT,
    signup_date    TEXT,
    customer_type  TEXT
);

CREATE TABLE products (
    product_id     INTEGER PRIMARY KEY,
    product_name   TEXT,
    category       TEXT,
    brand          TEXT,
    unit_price     REAL,
    cost_price     REAL
);

CREATE TABLE orders (
    order_id       INTEGER PRIMARY KEY,
    customer_id    INTEGER,
    product_id     INTEGER,
    order_date     TEXT,
    quantity       INTEGER,
    discount_pct   INTEGER,
    payment_mode   TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (product_id)  REFERENCES products(product_id)
);
""")

# ── Insert Customers (30 records) ─────────────────────────
customers_data = [
    (1,  'Priya Sharma',    'Mumbai',    'Maharashtra', 28, 'F', '2022-01-15', 'Premium'),
    (2,  'Rahul Verma',     'Delhi',     'Delhi',       35, 'M', '2022-03-20', 'Regular'),
    (3,  'Sneha Nair',      'Bangalore', 'Karnataka',   24, 'F', '2021-11-05', 'Regular'),
    (4,  'Amit Singh',      'Hyderabad', 'Telangana',   42, 'M', '2023-02-28', 'Premium'),
    (5,  'Kavita Patel',    'Chennai',   'Tamil Nadu',  31, 'F', '2022-07-10', 'Regular'),
    (6,  'Rohit Gupta',     'Pune',      'Maharashtra', 38, 'M', '2021-09-15', 'Premium'),
    (7,  'Meera Joshi',     'Kolkata',   'West Bengal', 22, 'F', '2023-01-01', 'Regular'),
    (8,  'Vikas Kumar',     'Ahmedabad', 'Gujarat',     29, 'M', '2022-05-20', 'Regular'),
    (9,  'Anjali Rao',      'Mumbai',    'Maharashtra', 45, 'F', '2021-12-30', 'Premium'),
    (10, 'Suresh Menon',    'Bangalore', 'Karnataka',   37, 'M', '2023-03-10', 'Regular'),
    (11, 'Divya Reddy',     'Hyderabad', 'Telangana',   26, 'F', '2022-08-22', 'Regular'),
    (12, 'Karan Malhotra',  'Delhi',     'Delhi',       33, 'M', '2021-10-14', 'Premium'),
    (13, 'Pooja Iyer',      'Chennai',   'Tamil Nadu',  29, 'F', '2023-04-05', 'Regular'),
    (14, 'Nikhil Desai',    'Pune',      'Maharashtra', 41, 'M', '2022-06-18', 'Premium'),
    (15, 'Shruti Bose',     'Kolkata',   'West Bengal', 27, 'F', '2023-02-12', 'Regular'),
    (16, 'Arun Tiwari',     'Mumbai',    'Maharashtra', 36, 'M', '2022-11-30', 'Regular'),
    (17, 'Ritu Pandey',     'Delhi',     'Delhi',       23, 'F', '2023-05-20', 'Regular'),
    (18, 'Sanjay Shah',     'Ahmedabad', 'Gujarat',     48, 'M', '2021-08-09', 'Premium'),
    (19, 'Lakshmi Nair',    'Bangalore', 'Karnataka',   32, 'F', '2022-09-15', 'Regular'),
    (20, 'Deepak Chopra',   'Mumbai',    'Maharashtra', 44, 'M', '2021-07-21', 'Premium'),
    (21, 'Nandini Verma',   'Delhi',     'Delhi',       25, 'F', '2023-06-08', 'Regular'),
    (22, 'Rajesh Kumar',    'Chennai',   'Tamil Nadu',  39, 'M', '2022-04-17', 'Regular'),
    (23, 'Smita Kulkarni',  'Pune',      'Maharashtra', 34, 'F', '2022-12-25', 'Premium'),
    (24, 'Varun Bajaj',     'Hyderabad', 'Telangana',   30, 'M', '2023-01-19', 'Regular'),
    (25, 'Geeta Mathur',    'Kolkata',   'West Bengal', 43, 'F', '2021-06-14', 'Premium'),
    (26, 'Harish Pillai',   'Bangalore', 'Karnataka',   28, 'M', '2022-10-03', 'Regular'),
    (27, 'Asha Goswami',    'Mumbai',    'Maharashtra', 51, 'F', '2021-05-28', 'Premium'),
    (28, 'Mukesh Trivedi',  'Delhi',     'Delhi',       37, 'M', '2022-02-16', 'Regular'),
    (29, 'Preeti Saxena',   'Ahmedabad', 'Gujarat',     26, 'F', '2023-07-11', 'Regular'),
    (30, 'Santosh Hegde',   'Bangalore', 'Karnataka',   46, 'M', '2021-04-22', 'Premium'),
]
cur.executemany("INSERT INTO customers VALUES (?,?,?,?,?,?,?,?)", customers_data)

# ── Insert Products (20 records) ──────────────────────────
products_data = [
    (1,  'Dell Laptop 15',      'Laptops',      'Dell',     72000,  52000),
    (2,  'HP Laptop 14',        'Laptops',      'HP',       58000,  41000),
    (3,  'Samsung Galaxy M54',  'Mobiles',      'Samsung',  28000,  19000),
    (4,  'Redmi Note 13',       'Mobiles',      'Xiaomi',   18000,  11000),
    (5,  'iPhone 14',           'Mobiles',      'Apple',    79000,  55000),
    (6,  'iPad 10th Gen',       'Tablets',      'Apple',    44000,  30000),
    (7,  'Samsung Tab A9',      'Tablets',      'Samsung',  22000,  14000),
    (8,  'Sony WH-1000XM5',     'Audio',        'Sony',     29000,  18000),
    (9,  'boAt Rockerz 450',    'Audio',        'boAt',     2500,   1200),
    (10, 'Logitech MX Master',  'Accessories',  'Logitech', 8500,   5000),
    (11, 'Keychron K2 Keyboard','Accessories',  'Keychron', 7200,   4500),
    (12, 'Dell 24" Monitor',    'Monitors',     'Dell',     18000,  12000),
    (13, 'LG 27" 4K Monitor',   'Monitors',     'LG',       32000,  21000),
    (14, 'WD 1TB External HDD', 'Storage',      'WD',       4500,   2800),
    (15, 'Samsung 512GB SSD',   'Storage',      'Samsung',  6500,   3800),
    (16, 'TP-Link Router AC750','Networking',   'TP-Link',  2200,   1300),
    (17, 'Epson L3252 Printer', 'Printers',     'Epson',    12000,  8000),
    (18, 'MS Office 365',       'Software',     'Microsoft',6999,   1000),
    (19, 'Antivirus Pro 1Yr',   'Software',     'Kaspersky',1999,    400),
    (20, 'USB-C Hub 7-in-1',    'Accessories',  'Anker',    3500,   1800),
]
cur.executemany("INSERT INTO products VALUES (?,?,?,?,?,?)", products_data)

# ── Insert Orders (80 records) ────────────────────────────
np.random.seed(42)
orders_data = []
order_id = 1001
dates = pd.date_range('2023-01-01','2023-12-31',periods=80)
dates = sorted([d.strftime('%Y-%m-%d') for d in dates])
payment_modes = ['UPI','Credit Card','Debit Card','Net Banking','EMI']
discounts     = [0, 0, 0, 5, 5, 10, 10, 15, 20]

for i,date in enumerate(dates):
    cust_id    = np.random.randint(1,31)
    prod_id    = np.random.randint(1,21)
    qty        = int(np.random.choice([1,1,1,2,2,3], p=[0.4,0.2,0.1,0.15,0.1,0.05]))
    disc       = int(np.random.choice(discounts))
    pay        = np.random.choice(payment_modes, p=[0.35,0.25,0.20,0.12,0.08])
    orders_data.append((order_id, cust_id, prod_id, date, qty, disc, pay))
    order_id += 1

cur.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?,?)", orders_data)
conn.commit()

print("    ✅ Database created:")
print("       customers table : 30 records")
print("       products table  : 20 records")
print("       orders table    : 80 records")

# ════════════════════════════════════════════════════════════
#  SECTION 2 — 10 SQL QUERIES
# ════════════════════════════════════════════════════════════
print("\n[2/5] Running SQL queries...")

# Q1 — Total Revenue & Profit by Category
q1 = """
SELECT
    p.category,
    COUNT(o.order_id)                                              AS total_orders,
    SUM(o.quantity)                                               AS units_sold,
    ROUND(SUM(o.quantity * p.unit_price * (1-o.discount_pct/100.0))/1000, 1) AS revenue_K,
    ROUND(SUM(o.quantity * (p.unit_price*(1-o.discount_pct/100.0) - p.cost_price))/1000, 1) AS profit_K,
    ROUND(AVG(o.discount_pct),1)                                  AS avg_discount
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.category
ORDER BY revenue_K DESC
"""

# Q2 — Top 10 Customers by Revenue (CLV)
q2 = """
SELECT
    c.customer_name,
    c.city,
    c.customer_type,
    COUNT(o.order_id)                                              AS total_orders,
    ROUND(SUM(o.quantity * p.unit_price * (1-o.discount_pct/100.0))/1000, 1) AS revenue_K,
    ROUND(AVG(o.quantity * p.unit_price * (1-o.discount_pct/100.0))/1000, 1) AS avg_order_K
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p  ON o.product_id  = p.product_id
GROUP BY c.customer_id
ORDER BY revenue_K DESC
LIMIT 10
"""

# Q3 — City-wise Sales Performance
q3 = """
SELECT
    c.city,
    c.state,
    COUNT(DISTINCT c.customer_id)                                 AS customers,
    COUNT(o.order_id)                                             AS orders,
    ROUND(SUM(o.quantity * p.unit_price * (1-o.discount_pct/100.0))/1000, 1) AS revenue_K
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p  ON o.product_id  = p.product_id
GROUP BY c.city
ORDER BY revenue_K DESC
LIMIT 8
"""

# Q4 — Monthly Revenue Trend
q4 = """
SELECT
    SUBSTR(o.order_date,1,7)                                      AS month,
    COUNT(o.order_id)                                             AS orders,
    ROUND(SUM(o.quantity * p.unit_price * (1-o.discount_pct/100.0))/1000, 1) AS revenue_K
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY month
ORDER BY month
"""

# Q5 — Payment Mode Analysis
q5 = """
SELECT
    payment_mode,
    COUNT(*)                                                       AS transactions,
    ROUND(100.0 * COUNT(*) / 80, 1)                               AS pct_share,
    ROUND(SUM(o.quantity * p.unit_price * (1-o.discount_pct/100.0))/1000, 1) AS revenue_K
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY payment_mode
ORDER BY transactions DESC
"""

# Q6 — Premium vs Regular Customer Comparison
q6 = """
SELECT
    c.customer_type,
    COUNT(DISTINCT c.customer_id)                                  AS customers,
    COUNT(o.order_id)                                              AS total_orders,
    ROUND(SUM(o.quantity * p.unit_price * (1-o.discount_pct/100.0))/1000, 1) AS total_revenue_K,
    ROUND(AVG(o.quantity * p.unit_price * (1-o.discount_pct/100.0))/1000, 2) AS avg_order_value_K
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN products p  ON o.product_id  = p.product_id
GROUP BY c.customer_type
"""

# Q7 — Top 5 Products by Revenue
q7 = """
SELECT
    p.product_name,
    p.category,
    p.brand,
    SUM(o.quantity)                                                AS units_sold,
    ROUND(SUM(o.quantity * p.unit_price * (1-o.discount_pct/100.0))/1000, 1) AS revenue_K
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.product_id
ORDER BY revenue_K DESC
LIMIT 5
"""

# Q8 — Repeat Purchase Rate (Window Function)
q8 = """
SELECT
    purchase_freq,
    COUNT(*) AS customers,
    ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 1) AS pct
FROM (
    SELECT
        customer_id,
        CASE
            WHEN COUNT(order_id) = 1 THEN 'One-time'
            WHEN COUNT(order_id) BETWEEN 2 AND 3 THEN 'Occasional (2-3x)'
            ELSE 'Loyal (4x+)'
        END AS purchase_freq
    FROM orders
    GROUP BY customer_id
) sub
GROUP BY purchase_freq
ORDER BY customers DESC
"""

# Q9 — Brand Performance
q9 = """
SELECT
    p.brand,
    COUNT(o.order_id)                                              AS orders,
    ROUND(SUM(o.quantity * p.unit_price * (1-o.discount_pct/100.0))/1000, 1) AS revenue_K,
    ROUND(AVG(o.discount_pct), 1)                                  AS avg_discount
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY p.brand
ORDER BY revenue_K DESC
LIMIT 8
"""

# Q10 — Running Total Revenue (Cumulative)
q10 = """
SELECT
    SUBSTR(order_date,1,7)                                         AS month,
    ROUND(SUM(o.quantity * p.unit_price * (1-o.discount_pct/100.0))/1000, 1) AS monthly_rev_K,
    ROUND(SUM(SUM(o.quantity * p.unit_price * (1-o.discount_pct/100.0)))
          OVER (ORDER BY SUBSTR(order_date,1,7))/1000, 1)         AS cumulative_rev_K
FROM orders o
JOIN products p ON o.product_id = p.product_id
GROUP BY month
ORDER BY month
"""

r1  = pd.read_sql(q1,  conn)
r2  = pd.read_sql(q2,  conn)
r3  = pd.read_sql(q3,  conn)
r4  = pd.read_sql(q4,  conn)
r5  = pd.read_sql(q5,  conn)
r6  = pd.read_sql(q6,  conn)
r7  = pd.read_sql(q7,  conn)
r8  = pd.read_sql(q8,  conn)
r9  = pd.read_sql(q9,  conn)
r10 = pd.read_sql(q10, conn)

print("    ✅ 10 SQL queries executed successfully")

# ════════════════════════════════════════════════════════════
#  SECTION 3 — KPI SUMMARY
# ════════════════════════════════════════════════════════════
print("\n[3/5] Computing KPIs...")

total_rev   = pd.read_sql("SELECT SUM(o.quantity*p.unit_price*(1-o.discount_pct/100.0)) FROM orders o JOIN products p ON o.product_id=p.product_id",conn).iloc[0,0]/1000
total_profit= pd.read_sql("SELECT SUM(o.quantity*(p.unit_price*(1-o.discount_pct/100.0)-p.cost_price)) FROM orders o JOIN products p ON o.product_id=p.product_id",conn).iloc[0,0]/1000
total_orders= 80
total_custs = 30
top_city    = r3.iloc[0]['city']
top_cat     = r1.iloc[0]['category']
top_payment = r5.iloc[0]['payment_mode']
top_cust    = r2.iloc[0]['customer_name']

print("\n"+"─"*60)
print("  📊 KEY PERFORMANCE INDICATORS — SQL ANALYTICS")
print("─"*60)
print(f"  💰 Total Revenue         : ₹{total_rev:.1f}K")
print(f"  💵 Total Profit          : ₹{total_profit:.1f}K")
print(f"  📦 Total Orders          : {total_orders}")
print(f"  👥 Total Customers       : {total_custs}")
print(f"  🏙️  Top City              : {top_city}")
print(f"  📱 Top Category          : {top_cat}")
print(f"  💳 Top Payment Mode      : {top_payment}")
print(f"  🏆 Top Customer          : {top_cust}")
print("─"*60)

for name, res in [
    ("Q1 — Category Revenue",    r1),
    ("Q2 — Top 10 Customers",    r2),
    ("Q3 — City Performance",    r3),
    ("Q4 — Monthly Trend",       r4),
    ("Q5 — Payment Modes",       r5),
    ("Q6 — Customer Type",       r6),
    ("Q7 — Top Products",        r7),
    ("Q8 — Repeat Purchase",     r8),
    ("Q9 — Brand Performance",   r9),
    ("Q10 — Cumulative Revenue", r10),
]:
    print(f"\n📋 {name}:\n{res.to_string(index=False)}")

# ════════════════════════════════════════════════════════════
#  SECTION 4 — DASHBOARD
# ════════════════════════════════════════════════════════════
print("\n[4/5] Building dashboard...")

fig = plt.figure(figsize=(20,11), facecolor=BG_DARK)
gs  = gridspec.GridSpec(2, 3, figure=fig, hspace=0.48, wspace=0.38)
ax1,ax2,ax3 = fig.add_subplot(gs[0,0]),fig.add_subplot(gs[0,1]),fig.add_subplot(gs[0,2])
ax4,ax5,ax6 = fig.add_subplot(gs[1,0]),fig.add_subplot(gs[1,1]),fig.add_subplot(gs[1,2])

# Chart 1 — Category Revenue Bar
bars1 = ax1.bar(r1['category'], r1['revenue_K'], color=ACCENT[:len(r1)], width=0.55, edgecolor='none')
ax1.set_title('📦 Revenue by Category (₹K)')
ax1.set_ylabel('Revenue (₹ Thousands)')
ax1.tick_params(axis='x', rotation=35)
ax1.grid(True, axis='y')
for bar,val in zip(bars1, r1['revenue_K']):
    ax1.text(bar.get_x()+bar.get_width()/2, bar.get_height()+5,
             f'₹{val}K', ha='center', fontsize=8, color=TEXT_C)

# Chart 2 — Monthly Revenue + Cumulative Line
ax2b = ax2.twinx()
ax2.bar(r4['month'], r4['revenue_K'], color=ACCENT[0], alpha=0.7, width=0.6, edgecolor='none', label='Monthly')
ax2b.plot(r4['month'], r10['cumulative_rev_K'], color=ACCENT[2], lw=2.5, marker='o', markersize=5, label='Cumulative')
ax2.set_title('📅 Monthly + Cumulative Revenue')
ax2.set_ylabel('Monthly Revenue (₹K)', color=ACCENT[0])
ax2b.set_ylabel('Cumulative (₹K)', color=ACCENT[2])
ax2.tick_params(axis='x', rotation=45)
ax2.grid(True, axis='y', alpha=0.3)

# Chart 3 — City Revenue Horizontal Bar
bars3 = ax3.barh(r3['city'], r3['revenue_K'], color=ACCENT[3:3+len(r3)], edgecolor='none', height=0.55)
ax3.set_title('🏙️  Top Cities by Revenue')
ax3.set_xlabel('Revenue (₹ Thousands)')
ax3.invert_yaxis()
ax3.grid(True, axis='x')
for bar,val in zip(bars3, r3['revenue_K']):
    ax3.text(bar.get_width()+2, bar.get_y()+bar.get_height()/2,
             f'₹{val}K', va='center', fontsize=9, color=TEXT_C)

# Chart 4 — Top 5 Customers
top5 = r2.head(5)
bars4 = ax4.barh(top5['customer_name'], top5['revenue_K'],
                 color=[ACCENT[0] if t=='Premium' else ACCENT[4] for t in top5['customer_type']],
                 edgecolor='none', height=0.55)
ax4.set_title('🏆 Top 5 Customers (CLV)')
ax4.set_xlabel('Revenue (₹ Thousands)')
ax4.invert_yaxis()
ax4.grid(True, axis='x')
for bar,val in zip(bars4, top5['revenue_K']):
    ax4.text(bar.get_width()+1, bar.get_y()+bar.get_height()/2,
             f'₹{val}K', va='center', fontsize=9, color=TEXT_C)
from matplotlib.patches import Patch
ax4.legend(handles=[Patch(color=ACCENT[0],label='Premium'),
                    Patch(color=ACCENT[4],label='Regular')], fontsize=8)

# Chart 5 — Payment Mode Donut
wedges,texts,autotexts = ax5.pie(
    r5['transactions'], labels=r5['payment_mode'], autopct='%1.1f%%',
    colors=ACCENT[:len(r5)], startangle=90,
    wedgeprops=dict(width=0.55, edgecolor=BG_DARK, linewidth=2),
    pctdistance=0.75)
for at in autotexts: at.set_fontsize(9); at.set_fontweight('bold')
ax5.set_title('💳 Payment Mode Share')

# Chart 6 — Repeat Purchase
colors6 = [ACCENT[3], ACCENT[2], ACCENT[0]]
bars6 = ax6.bar(r8['purchase_freq'], r8['customers'],
                color=colors6[:len(r8)], width=0.45, edgecolor='none')
ax6.set_title('🔁 Customer Purchase Frequency')
ax6.set_ylabel('Number of Customers')
ax6.grid(True, axis='y')
for bar,val,pct in zip(bars6, r8['customers'], r8['pct']):
    ax6.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.2,
             f'{val}\n({pct}%)', ha='center', fontsize=9, color=TEXT_C)

# Title strip
fig.text(0.5,0.98,'🛒  Customer Purchase Behaviour — SQL Analytics Dashboard',
         ha='center',va='top',fontsize=16,fontweight='bold',color=TEXT_C,family='monospace')
fig.text(0.5,0.955,
         f'Revenue: ₹{total_rev:.0f}K   |   Profit: ₹{total_profit:.0f}K   |   '
         f'Orders: {total_orders}   |   Customers: {total_custs}   |   Top City: {top_city}',
         ha='center',va='top',fontsize=10,color=SUB_C,family='monospace')

# ════════════════════════════════════════════════════════════
#  SECTION 5 — SAVE
# ════════════════════════════════════════════════════════════
print("[5/5] Saving files...")
plt.savefig('sql_analytics_dashboard.png', dpi=160, bbox_inches='tight', facecolor=BG_DARK)

# Export all tables to CSV
pd.read_sql("SELECT * FROM customers", conn).to_csv('customers.csv', index=False)
pd.read_sql("SELECT * FROM products",  conn).to_csv('products.csv',  index=False)
pd.read_sql("SELECT * FROM orders",    conn).to_csv('orders.csv',    index=False)

print("\n"+"="*60)
print("  ✅ Files saved:")
print("     📊 sql_analytics_dashboard.png")
print("     📄 customers.csv | products.csv | orders.csv")
print("="*60)
conn.close()
plt.show()
