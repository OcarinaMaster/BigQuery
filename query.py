import streamlit as st
from google.cloud import bigquery
from google.oauth2 import service_account
import pandas as pd
import db_dtypes
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["gcp_service_account"]
)
st.set_page_config(
    page_title="Sales Viewer from BigQuery",
    layout="wide"  # Options are "centered" or "wide"
)
client = bigquery.Client(credentials=credentials)
start_date = st.date_input('Start date')
end_date = st.date_input('End date')
start_date_str = start_date.strftime("%Y-%m-%d")
end_date_str = end_date.strftime('%Y-%m-%d')
QUERY = (f'''SELECT * 
            FROM `supply-chain-382719.MMISDB_RPT.all_vouchers_v1` 
            WHERE INVOICE_DT BETWEEN '{start_date}' AND '{end_date}' 
            LIMIT 1000''')
if 'clicked' not in st.session_state:
     st.session_state.clicked = False
def click_button():
    st.session_state.clicked = True
def paginate_dataframe(df, page, page_size):
        start = (page - 1) * page_size
        end = start + page_size
        return df[start:end]
st.button('Search', on_click=click_button)

if st.session_state.clicked:
    table = client.query(QUERY).result()
    df = table.to_dataframe()

    #df = table.to_dataframe()

    # Pagination parameters
    page_size = st.sidebar.slider("Page size", min_value=10, max_value=100, value=50)
    total_pages = (len(df) + page_size - 1) // page_size

    page = st.sidebar.slider("Page", min_value=1, max_value=total_pages, value=1)

    paginated_df = paginate_dataframe(df, page, page_size)

    st.write(f"Showing page {page} of {total_pages}")
    st.dataframe(paginated_df, width = 2400, height = 1000)
