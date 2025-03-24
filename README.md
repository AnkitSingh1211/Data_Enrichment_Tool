# Data Enrichment Tool
### Link: https://data-enrichment-tool.streamlit.app
## 🚀 Overview
This is a **Streamlit-based** web application that allows users to:
- **Upload CSV datasets** and interact with them.
- **Convert Natural Language (NL) queries into SQL** using Google's Gemini AI.
- **Run SQL queries** directly on the uploaded datasets.
- **Compute Key Business Metrics** such as:
  - **Click-Through Rate (CTR)**
  - **Churn Rate**
  - **Customer Lifetime Value (CLV)**
- **View and analyze query results in real time**.

## 📌 Features
- **Upload & Preview CSV Files**: Users can upload multiple datasets and view their first few rows.
- **Natural Language to SQL**: Convert text-based queries into SQL queries dynamically.
- **Execute SQL Queries**: Run the generated SQL queries on the uploaded datasets.
- **Compute Business Metrics**:
  - **CTR Formula:**
    ```
    CTR = (Clicks on Campaign / Impressions) * 100
    ```
  - **Churn Rate Formula:**
    ```
    Churn Rate = (Customers Lost in Period / Total Customers at Start of Period) * 100
    ```
  - **CLV Formula:**
    ```
    CLV = (Average Purchase Value) * (Purchase Frequency) * (Customer Lifespan)
    ```
- **Interactive UI**: Built with Streamlit for a seamless user experience.

## 🛠️ Installation & Setup
### 1️⃣ Clone the Repository
```sh
 git clone [https://github.com/AnkitSingh1211/Data_Enrichment_Tool.git]
 cd Data_Enrichment_Tool
