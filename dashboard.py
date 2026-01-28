import plotly_express as px
import streamlit as st
from tracker import get_data , get_sector
   
value = []
st.set_page_config(page_title="My Portfolio", layout="wide")
st.title("🚀 quantitative-portfolio-analyzer")

with st.spinner("Crunching the numbers..."):
    portfolio_table, current_value, invested_value, banchmark = get_data()
    sector_df = get_sector()

with st.container(border=True):
    col1, col2, col3 =st.columns(3)
    col1.metric("Total Investment", f"₹{invested_value:,.0f}")
    col2.metric("Current Investment", f"₹{current_value:,.0f}")
    Total = current_value-invested_value
    col3.metric("Total P&L", f"₹{Total:+,.2f}")


with st.container(border=True):
    co1, co2 =st.columns(2)
    with co1:
        co1.subheader("Stock-Distribution")
        fig1 = px.pie(portfolio_table, names=portfolio_table.index, values ="Alocation %")
        st.plotly_chart(fig1, use_container_width=True)
    with co2:
        co2.subheader("Sector-Distribution")
        fig2 = px.pie(sector_df, names= sector_df["Sector"])
        st.plotly_chart(fig2, use_container_width=True)
        

with st.container(border=True):
    table_height = (len(portfolio_table)+1)*35 
    st.subheader("Holdings:")
    st.dataframe(portfolio_table,use_container_width=True,height=table_height)