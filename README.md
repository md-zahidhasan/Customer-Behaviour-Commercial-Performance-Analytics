# Customer Behaviour & Commercial Performance Analytics

## Project Overview

**Customer Behaviour & Commercial Performance Analytics** is an interactive business intelligence and customer analytics project designed to analyze customer behaviour, sales performance, transaction patterns, marketing offers, and customer journeys.

The project follows a structured analytics workflow:

**Raw Data → SQL Database & Analysis → Python/Pandas → Streamlit → Plotly Interactive Dashboard**

The objective is to transform raw customer and transaction data into meaningful business insights that can support customer segmentation, sales analysis, offer performance evaluation, and commercial decision-making.

---

## Business Objectives

The project focuses on answering important business questions such as:

* How are overall sales and transaction volumes performing?
* Which customer groups generate the highest revenue?
* What are the purchasing patterns of different customer segments?
* How does customer income relate to spending behaviour?
* Which membership or demographic groups are most commercially valuable?
* Which marketing offers receive the most engagement?
* How effective is the offer conversion funnel?
* How do customers move through different stages of the customer journey?
* Which customers have high transaction frequency or spending?
* Which products, offers, or customer groups require further attention?
* How can customer data be transformed into actionable commercial insights?

---

# Project Architecture

The project is designed around a modern analytics pipeline:

```text
                 Raw CSV / CSV.GZ Files
                         │
                         ▼
                 Data Preparation
                  Python / Pandas
                         │
                         ▼
                   SQLite Database
                         │
                         ▼
                    SQL Analysis
          ┌──────────────┼──────────────┐
          │              │              │
     Customer SQL    Sales SQL      Offer SQL
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                  Python / Pandas
                         │
                         ▼
                Streamlit Dashboard
                         │
                         ▼
               Plotly Visualizations
```

This architecture separates data storage, analytical querying, data processing, and visualization.

---

# Key Features

## 1. Executive Overview

The Executive Overview provides a high-level summary of commercial performance through important KPIs.

Typical KPIs include:

* Total Sales
* Total Transactions
* Average Transaction Value
* Total Customers
* Active Customers
* Customer Engagement
* Offer Response Rate
* Conversion Rate

These metrics allow users to quickly understand the overall business situation.

---

# 2. Sales & Transaction Analytics

The Sales & Transactions section analyzes purchasing and transaction behaviour.

It can provide insights into:

* Total sales
* Transaction volume
* Average transaction value
* Customer spending
* Transaction frequency
* Sales distribution
* Customer-level purchasing behaviour
* Revenue contribution by customer segment

### Example SQL Analysis

```sql
SELECT
    customer_id,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_spend,
    AVG(amount) AS average_transaction
FROM events
WHERE event = 'transaction'
GROUP BY customer_id
ORDER BY total_spend DESC;
```

This query identifies customers based on their transaction frequency and spending behaviour.

---

# 3. Customer Analytics

Customer Analytics focuses on understanding customer characteristics and commercial value.

The analysis can include:

* Customer demographics
* Gender distribution
* Age distribution
* Income distribution
* Membership information
* Customer spending
* Transaction frequency
* Customer segmentation

Customers can be compared based on demographic and behavioural characteristics.

For example:

```text
Customer Demographics
        ↓
Income & Membership
        ↓
Transaction Behaviour
        ↓
Customer Value
```

This helps identify different customer groups and their commercial characteristics.

---

# 4. Customer Segmentation

Customer segmentation allows customers to be grouped based on their behaviour and characteristics.

Possible segments include:

* High-value customers
* Frequent customers
* Low-frequency customers
* High-spending customers
* Low-spending customers
* Highly engaged customers
* Offer-responsive customers

A customer-level analytical table can be generated using SQL and then processed with Python.

Example:

```sql
SELECT
    customer_id,
    COUNT(*) AS transaction_count,
    SUM(amount) AS total_spend,
    AVG(amount) AS average_spend
FROM events
WHERE event = 'transaction'
GROUP BY customer_id;
```

Python can then use these results for further analysis and visualization.

---

# 5. Offer Performance Analytics

The Offer Performance section analyzes marketing and promotional activities.

Important metrics can include:

* Number of offers
* Offer types
* Offer views
* Offer received
* Offer completion
* Offer conversion
* Response rate
* Conversion rate
* Customer engagement

The offer funnel can be represented as:

```text
Offers Sent
     ↓
Offers Viewed
     ↓
Offers Engaged
     ↓
Offers Completed
     ↓
Conversions
```

This helps evaluate how customers interact with promotional campaigns.

---

# 6. Offer Conversion Analysis

SQL can be used to calculate offer-level performance.

Example:

```sql
SELECT
    offer_id,
    COUNT(*) AS total_events,
    SUM(
        CASE
            WHEN event = 'offer completed'
            THEN 1
            ELSE 0
        END
    ) AS completed_offers
FROM events
GROUP BY offer_id;
```

Python can then calculate conversion rates and create interactive visualizations.

---

# 7. Customer Journey Analytics

The Customer Journey section analyzes how customers interact with the business over time.

A simplified customer journey can be represented as:

```text
Customer
   ↓
Offer Received
   ↓
Offer Viewed
   ↓
Customer Engaged
   ↓
Transaction
   ↓
Offer Completed
```

This allows the project to examine customer interaction across different stages.

The analysis can help identify:

* Engagement patterns
* Drop-off points
* Transaction behaviour
* Offer response
* Conversion behaviour

---

# 8. Demographic Analysis

The dashboard provides interactive analysis based on customer demographics.

Important dimensions include:

* Gender
* Age
* Income
* Membership date
* Customer groups

For example, users can compare:

```text
Income Group
      ↓
Average Spending
      ↓
Transaction Frequency
      ↓
Customer Value
```

This makes it possible to investigate relationships between customer characteristics and commercial performance.

---

# 9. Interactive Filters

The Streamlit dashboard provides interactive filters so users can dynamically explore the dataset.

Possible filters include:

* Gender
* Age
* Income
* Membership Date
* Offer Type
* Customer ID
* Event Type

When a filter is changed, the dashboard updates the relevant metrics, tables, and charts.

---

# 10. Data Explorer

The Data Explorer section allows users to inspect the underlying analytical data.

Users can explore:

* Customer records
* Transaction records
* Offer records
* Event data
* SQL query results
* Filtered datasets

This provides transparency between the underlying data and dashboard results.

---

# SQL Analytics Layer

SQL is used as the analytical query layer between the database and Python.

The project can use **SQLite** because it is lightweight and does not require a separate database server.

Example database structure:

```text
SQLite Database
│
├── customers
│
├── events
│
└── offers
```

### Customers Table

Contains customer-level information such as:

* Customer ID
* Gender
* Age
* Income
* Membership information

### Events Table

Contains customer interaction and transaction events such as:

* Customer ID
* Event
* Offer ID
* Amount
* Time

### Offers Table

Contains information about marketing offers such as:

* Offer ID
* Offer Type
* Offer details
* Offer duration
* Reward

---

# SQL Query Examples

## Customer Spending

```sql
SELECT
    customer_id,
    SUM(amount) AS total_spend
FROM events
WHERE event = 'transaction'
GROUP BY customer_id
ORDER BY total_spend DESC;
```

## Transaction Frequency

```sql
SELECT
    customer_id,
    COUNT(*) AS transaction_count
FROM events
WHERE event = 'transaction'
GROUP BY customer_id
ORDER BY transaction_count DESC;
```

## Average Transaction Value

```sql
SELECT
    AVG(amount) AS average_transaction_value
FROM events
WHERE event = 'transaction';
```

## Sales by Customer

```sql
SELECT
    customer_id,
    COUNT(*) AS transactions,
    SUM(amount) AS revenue,
    AVG(amount) AS avg_transaction
FROM events
WHERE event = 'transaction'
GROUP BY customer_id;
```

---

# Python Analytics Layer

Python is used to connect the SQL analysis with the dashboard.

Main responsibilities include:

* Loading data
* Data cleaning
* Data transformation
* Database preparation
* Executing SQL queries
* Reading SQL results
* KPI calculation
* Data validation
* Visualization preparation
* Streamlit application logic

The primary libraries include:

* Pandas
* NumPy
* SQLite3
* Plotly
* Streamlit

Example Python-SQL integration:

```python
import sqlite3
import pandas as pd

conn = sqlite3.connect("analytics.db")

query = """
SELECT
    customer_id,
    SUM(amount) AS total_spend
FROM events
WHERE event = 'transaction'
GROUP BY customer_id
ORDER BY total_spend DESC
"""

df = pd.read_sql_query(query, conn)
```

The SQL result can then be passed directly into Plotly or Streamlit.

---

# Streamlit Dashboard

Streamlit is used to convert the analytical workflow into an interactive web-based dashboard.

The dashboard can contain multiple analytical sections:

```text
Customer Behaviour & Commercial Performance
│
├── Executive Overview
├── Sales & Transactions
├── Customer Analytics
├── Offer Performance
├── Customer Journey
└── Data Explorer
```

Users can interact with filters and visualizations without directly working with SQL or Python code.

---

# Data Visualization

Plotly is used to create interactive visualizations.

Possible charts include:

### Sales Analysis

* Sales trend
* Revenue distribution
* Transaction volume
* Average transaction value

### Customer Analysis

* Customer segmentation
* Spending distribution
* Income vs spending
* Age distribution
* Customer value analysis

### Offer Analysis

* Offer performance
* Offer conversion
* Offer engagement
* Offer funnel

### Customer Journey

* Event distribution
* Customer engagement
* Journey funnel
* Conversion analysis

---

# Technology Stack

| Technology   | Purpose                                   |
| ------------ | ----------------------------------------- |
| Python       | Data processing and application logic     |
| SQL          | Data querying and analytical calculations |
| SQLite       | Relational analytical database            |
| Pandas       | Data manipulation                         |
| NumPy        | Numerical analysis                        |
| Streamlit    | Interactive dashboard                     |
| Plotly       | Interactive visualization                 |
| CSV / CSV.GZ | Raw data storage                          |
| Git & GitHub | Version control and project hosting       |

---

# Project Structure

```text
Customer-Behaviour-Commercial-Performance-Analytics/
│
├── app.py
│
├── prepare_data.py
│
├── sql/
│   ├── customer_analysis.sql
│   ├── sales_analysis.sql
│   ├── offer_analysis.sql
│   └── customer_journey.sql
│
├── data/
│   ├── customer_master_full1.csv
│   ├── events_clean.csv.gz
│   └── offers.csv
│
├── analytics.db
│
├── requirements.txt
│
└── README.md
```

---

# Data Preparation

The data preparation process includes:

1. Loading raw CSV files.
2. Reading compressed CSV data.
3. Handling missing values.
4. Standardizing column names.
5. Converting data types.
6. Preparing customer, event, and offer datasets.
7. Loading cleaned datasets into SQLite.
8. Creating SQL analytical queries.
9. Connecting SQL results with Python.
10. Building the Streamlit dashboard.

---

# Analytical Workflow

The complete workflow is:

### Step 1 — Raw Data

Customer, event, transaction, and offer datasets are collected from CSV/CSV.GZ files.

### Step 2 — Data Preparation

Python and Pandas are used to clean and prepare the datasets.

### Step 3 — Database Creation

The cleaned datasets are loaded into SQLite tables.

### Step 4 — SQL Analysis

SQL queries calculate:

* Customer metrics
* Sales metrics
* Transaction metrics
* Offer metrics
* Engagement metrics
* Customer journey metrics

### Step 5 — Python Processing

Python retrieves SQL results and performs additional calculations and transformations.

### Step 6 — Visualization

Plotly converts analytical results into interactive charts.

### Step 7 — Dashboard

Streamlit presents the results through an interactive business intelligence dashboard.

---

# Installation

## 1. Clone the Repository

```bash
git clone https://github.com/md-zahidhasan/Customer-Behaviour-Commercial-Performance-Analytics.git
```

## 2. Navigate to the Project

```bash
cd Customer-Behaviour-Commercial-Performance-Analytics
```

## 3. Create a Virtual Environment

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### macOS / Linux

```bash
source venv/bin/activate
```

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Running the Project

First prepare the database:

```bash
python prepare_data.py
```

Then run the Streamlit application:

```bash
streamlit run app.py
```

The dashboard will open in the browser.

---

# Example KPI Framework

The dashboard can calculate metrics such as:

### Total Revenue

```text
Total Revenue = SUM(Transaction Amount)
```

### Transaction Count

```text
Transaction Count = Number of Transaction Events
```

### Average Transaction Value

```text
Average Transaction Value
= Total Revenue / Total Transactions
```

### Customer Spend

```text
Customer Spend
= SUM(Customer Transaction Amount)
```

### Offer Conversion Rate

```text
Conversion Rate
= Completed Offers / Received Offers × 100
```

These metrics can be calculated through SQL and further processed through Python.

---

# Business Questions

This project is designed to answer questions such as:

### Customer Behaviour

* Who are the highest-spending customers?
* Which customers make transactions most frequently?
* How does income relate to spending?
* Which demographic groups show different purchasing patterns?

### Commercial Performance

* What is the total sales performance?
* What is the average transaction value?
* Which customers contribute most to revenue?
* How does transaction activity vary across customer segments?

### Marketing & Offers

* Which offer types receive the most engagement?
* Which offers have higher completion rates?
* How many customers move from receiving an offer to completing it?
* Where do customers drop out of the offer funnel?

### Customer Journey

* How do customers interact with offers?
* Which events occur most frequently?
* How does engagement translate into transactions?
* What patterns can be observed across the customer journey?

---

# Project Benefits

The project demonstrates an end-to-end data analytics workflow rather than only creating charts.

It combines:

```text
Data Engineering
        +
SQL Analytics
        +
Python Analytics
        +
Business Intelligence
        +
Interactive Visualization
```

This makes the project suitable for demonstrating practical skills in:

* Data Analytics
* SQL
* Python
* Pandas
* Data Visualization
* Business Intelligence
* Customer Analytics
* Commercial Analytics
* Streamlit Dashboard Development

---

# Skills Demonstrated

### SQL

* SELECT statements
* Filtering
* Aggregation
* GROUP BY
* CASE statements
* Analytical queries
* Customer-level aggregation
* Transaction analysis
* Offer analysis

### Python

* Pandas
* NumPy
* Data cleaning
* Data transformation
* SQL integration
* KPI calculations
* Application development

### Visualization

* Plotly
* Interactive charts
* KPI cards
* Filters
* Trend analysis
* Distribution analysis
* Funnel analysis

### Streamlit

* Dashboard development
* Sidebar filters
* Interactive components
* Data tables
* KPI presentation
* Multi-section analytics interface

---

# Future Improvements

Potential future enhancements include:

* Advanced customer segmentation
* RFM analysis
* Customer lifetime value analysis
* Churn prediction
* Customer propensity modeling
* Automated reporting
* Advanced marketing campaign analysis
* Machine learning-based customer segmentation
* Predictive sales analytics
* Cloud database integration
* Automated data pipelines
* Deployment through Streamlit Cloud

---

# Project Objective

The main objective of this project is to demonstrate how raw customer and commercial data can be transformed into a structured analytical solution.

The project connects:

**SQL for data querying → Python for analytical processing → Plotly for visualization → Streamlit for interactive business intelligence.**

This provides an end-to-end framework for exploring customer behaviour and commercial performance through data-driven analysis.

---

# Author

**Md Zahid Hasan**

GitHub:
https://github.com/md-zahidhasan

---

# License

This project is intended for educational, portfolio, and analytical demonstration purposes.



