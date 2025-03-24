import streamlit as st
import google.generativeai as genai
import sqlglot
import pandas as pd
import sqlite3
import re

# Configure Gemini API Key
GENAI_API_KEY = "AIzaSyDR7EHbZ3b1wf3R_YRPoOYPQPBAezKZ5ac"
genai.configure(api_key=GENAI_API_KEY)


def clean_sql_output(sql_text):
    """Cleans the generated SQL by removing unnecessary formatting."""
    return re.sub(r'```sql|```', '', sql_text).strip()


def format_table_name(dataset_name):
    """Formats dataset names to be SQLite-compatible."""
    return dataset_name.replace("-", "_").replace(" ", "_").replace(".", "_")


def format_column_names(df):
    """Formats column names to be SQLite-compatible."""
    df.columns = [col.replace(" ", "_").replace("-", "_") for col in df.columns]
    return df


def get_column_names(datasets):
    """Extract column names for each dataset."""
    return {format_table_name(name): list(df.columns) for name, df in datasets.items()}


def nl_to_sql(user_query, dataset_info):
    formatted_names = [f"{table} ({', '.join(cols)})" for table, cols in dataset_info.items()]
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content(
        f"Convert this to SQL using datasets: {', '.join(formatted_names)}. Only return raw SQL query without explanations: {user_query}")
    return clean_sql_output(response.text)


def run_sql_on_dataset(sql_query, datasets):
    try:
        conn = sqlite3.connect(":memory:")
        cursor = conn.cursor()

        for dataset_name, df in datasets.items():
            table_name = format_table_name(dataset_name)
            df = format_column_names(df)
            df.to_sql(table_name, conn, index=False, if_exists="replace")

        result_df = pd.read_sql_query(sql_query, conn)
        conn.close()
        return result_df
    except Exception as e:
        return f"Error executing SQL: {str(e)}"


def calculate_metrics(df):
    """Calculate CTR, Churn Rate, and CLV if relevant columns exist."""
    metrics = {}

    if {'Campaign_Impressions', 'Clicks_on_Campaign'}.issubset(df.columns):
        metrics['CTR'] = (df['Clicks_on_Campaign'].sum() / df['Campaign_Impressions'].sum()) * 100

    if {'Total_Customers_Start', 'Customers_Lost'}.issubset(df.columns):
        metrics['Churn_Rate'] = (df['Customers_Lost'].sum() / df['Total_Customers_Start'].sum()) * 100

    if {'Average_Purchase_Value', 'Purchase_Frequency', 'Customer_Lifespan'}.issubset(df.columns):
        metrics['CLV'] = (df['Average_Purchase_Value'].mean() *
                          df['Purchase_Frequency'].mean() *
                          df['Customer_Lifespan'].mean())

    return metrics


# Streamlit UI
st.title("💡 Data Enrichment Tool")

uploaded_files = st.file_uploader("Upload CSV files", accept_multiple_files=True, type=["csv"])
datasets = {}

if uploaded_files:
    for file in uploaded_files:
        formatted_name = format_table_name(file.name)
        df = pd.read_csv(file)
        df = format_column_names(df)
        datasets[formatted_name] = df
    st.write("### Preview of Uploaded Datasets")
    for name, df in datasets.items():
        st.subheader(name)
        st.dataframe(df.head())

# Convert NL to SQL
user_query = st.text_area("Enter your question:")
if st.button("Convert to SQL and Run"):
    if user_query and datasets:
        dataset_info = get_column_names(datasets)
        sql_query = nl_to_sql(user_query, dataset_info)
        st.code(sql_query, language='sql')

        result = run_sql_on_dataset(sql_query, datasets)
        if isinstance(result, pd.DataFrame):
            st.write("### Query Results")
            st.dataframe(result)
        else:
            st.error(result)
    else:
        st.warning("Please enter a query and upload at least one dataset.")

# Compute Metrics
if st.button("Compute Metrics"):
    for name, df in datasets.items():
        st.subheader(f"Metrics for {name}")
        metrics = calculate_metrics(df)
        if metrics:
            for key, value in metrics.items():
                st.write(f"**{key}:** {value:.2f}")
        else:
            st.write("No relevant data found for CTR, Churn Rate, or CLV calculation.")
