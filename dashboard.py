import plotly_express as px
import streamlit as st
from tracker import get_data
   
value = []
st.set_page_config(page_title="My Portfolio", layout="wide")
st.title("🚀 quantitative-portfolio-analyzer")

with st.spinner("Crunching the numbers..."):
    portfolio_table, current_value, invested_value = get_data()

col1, col2, col3 =st.columns(3)

col1.metric("Total Investment", f"₹{invested_value:,.0f}")
col2.metric("Current Investment", f"₹{current_value:,.0f}")
Total = current_value-invested_value
col3.metric("Total P&L", f"₹{Total:+,.2f}")

table_height = (len(portfolio_table)+1)*35 
st.subheader("Holdings:")
st.dataframe(portfolio_table,use_container_width=True,height=table_height)
