import plotly_express as px
import streamlit as st
from tracker import get_data , get_sector
   
value = []
st.set_page_config(page_title="My Portfolio", layout="wide")
st.title("🚀 quantitative-portfolio-analyzer")

with st.spinner("Crunching the numbers..."):
    portfolio_table, portfolio_total, invested_value = get_data()
    current_value = portfolio_total["Total"].dropna().iloc[36]


    
with st.container(border=True):
    col1, col2, col3 =st.columns(3)
    col1.metric("Total Investment", f"₹{invested_value:,.0f}")
    col2.metric("Current Investment", f"₹{current_value:,.0f}")
    Total = current_value-invested_value
    col3.metric("Total P&L", f"₹{Total:+,.2f}")

col_1,col_2 =st.columns(2)

with col_1:
    with st.container(border=True):
    
        df_norm = portfolio_total.copy()

        df_norm['Total_Pct'] = (df_norm['Total'] / df_norm['Total'].iloc[0]) * 100
        df_norm['Nifty_Pct'] = (df_norm['Nifty'] / df_norm['Nifty'].iloc[0]) * 100

        fig_norm = px.line(
                df_norm.reset_index(), 
                x=df_norm.index.name or "Date", 
                y=['Total_Pct', 'Nifty_Pct'],
                title="Relative Performance: Portfolio vs Nifty (Base 100)",
                labels={"value": "Growth (%)", "variable": "Asset"})

        fig_norm.update_layout(xaxis_fixedrange=True, yaxis_fixedrange=True)
        st.plotly_chart(fig_norm, use_container_width=True)

with col_2:
    with st.container(border=True):

        df_clean = portfolio_table.reset_index()
        fig1 = px.sunburst(df_clean, 
                path=["Sector","Symbol"], 
                values ="Alocation %", 
                title= 'Stock-Distribution',)

        fig1.update_traces(textinfo="label+percent entry")
        fig1.update_layout(margin=dict(t=40, l=0, r=0, b=0))

        st.plotly_chart(fig1, use_container_width=True)


with st.container(border=True):
    table_height = (len(portfolio_table)+1)*35 
    st.subheader("Holdings:")
    st.dataframe(portfolio_table,use_container_width=True,height=table_height)

