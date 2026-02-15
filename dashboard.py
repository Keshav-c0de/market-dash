import plotly_express as px
import streamlit as st
import csv
from tracker import get_data , get_sector, is_valid_symbol, add_stock
   
value = []
st.set_page_config(page_title="My Portfolio", layout="wide")
st.title("🚀 quantitative-portfolio-analyzer")


with st.spinner("Crunching the numbers..."):
    portfolio_table, portfolio_total, invested_value, fundaments, df_metrics = get_data()
    current_value = portfolio_total["Total"].dropna().iloc[-1]


    
with st.container(border=True):
    col1, col2, col3 =st.columns(3)
    col1.metric("Total Investment", f"₹{invested_value:,.0f}")
    col2.metric("Current Investment", f"₹{current_value:,.0f}")
    Total = current_value-invested_value
    col3.metric("Total P&L", f"₹{Total:+,.2f}")


with st.container(border=True):
    col_alpha, col_beta, col_delta =st.columns(3)
    weights = portfolio_table["Alocation %"]/100
    metrics = df_metrics.set_index("Symbol")
    weighted_alpha = (metrics["Alpha"] * (portfolio_table["Alocation %"] / 100)).sum()
    weighted_beta = (metrics["Beta"] * (portfolio_table["Alocation %"] / 100)).sum()
    avg_momentum = df_metrics["Momentum Score 30D"].mean()
    col_alpha.metric("Weighted Alpha", f"{weighted_alpha:.2f}")
    col_beta.metric("Weighted Beta", f"{weighted_beta:.2f}")
    col_delta.metric("Avg Momentum", f"{avg_momentum:.2f}")

col_1,col_2 =st.columns(2)

with col_1:
    with st.container(border=True):
    
        df_norm = portfolio_total.copy()

        df_norm['Portfolio_Pct'] = (df_norm['Total'] / df_norm['Total'].iloc[0]) * 100
        df_norm['Nifty_Pct'] = (df_norm['Nifty'] / df_norm['Nifty'].iloc[0]) * 100

        fig_norm = px.line(
                df_norm.reset_index(), 
                x=df_norm.index.name or "Date", 
                y=['Portfolio_Pct', 'Nifty_Pct'],
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

if "show_form" not in st.session_state:
    st.session_state.show_form = False
if st.button("button"): 
    st.session_state.show_form = not st.session_state.show_form

if st.session_state.show_form:
    with st.container(border=True):
        col_symbol, col_quantity, col_price =st.columns(3)
        with col_symbol:
            symbol =st.text_input("Enter the Symbol","TCS.NS").upper()
        with col_quantity:
            quantity =st.number_input("Enter the Quantity",min_value=1,value=2,key="placeholder")
        with col_price:
            price =st.number_input("Enter the Buying Price",min_value=0.0,value=1900.0,key="laceholder")
        if st.button("CONFIRM ADD"):
            if is_valid_symbol(symbol):
                add_stock(symbol,quantity,price)
                st.session_state.show_form = False
                st.rerun()
            else:
                st.error(f"{symbol}is not corret Symbol")


with st.container(border=True):
    table_height = (len(fundaments)+1)*35 
    st.subheader("Holdings:")
    st.dataframe(fundaments,use_container_width=True,height=table_height)


'''with st.status(Transcrips):
    with st.container(border=True):
        pass'''
