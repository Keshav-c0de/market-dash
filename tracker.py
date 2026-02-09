import yfinance as yf
import pandas as pd
import time

def get_data():

    name_list = []
    beta = []
    market_annual_return = 0.1
    RISK_FREE_RATE = 0.06
    result =[]

    # Getting Data
    df = pd.read_csv("portfolio.csv")
    name_list = df['Symbol'].tolist()
    df.set_index("Symbol", inplace=True)
    if "^NSEI" not in name_list:
        name_list.append("^NSEI")
    stock =yf.download(name_list,period ="1y")
    price = stock["Close"]
    portfolio_total =get_chart_data(price,df['Quantity'])
    banchmark_total =price["^NSEI"]
    daily_returns =price.pct_change()
    df_stock =pd.DataFrame(daily_returns)
    df_stock =df_stock.dropna()
    banchmark = df_stock["^NSEI"]
    portfolio = df_stock.drop(columns=["^NSEI"])

    # Calculations
    years = 1
    variance = banchmark.var()
    benchmark_mom = banchmark.tail(30)
    Benchmark_mom_return = (benchmark_mom + 1).prod() - 1
    for stocks in portfolio.columns:
        stock_data = portfolio[stocks]

        # Calculate beta
        covariance = stock_data.cov(banchmark)
        beta =(covariance/variance)

        # Annual Return Calculation
        stock_annual_return = stock_data.mean() * 252 * years

        # Calculate alpha
        expected_return = RISK_FREE_RATE + beta * (market_annual_return - RISK_FREE_RATE)
        alpha = stock_annual_return - expected_return

        # momentum
        stock_mom = stock_data.tail(30)
        stock_mom_return = (stock_mom + 1).prod() - 1
        mom_score =(stock_mom_return - Benchmark_mom_return) * 100

        result.append({
            "Symbol": stocks,
            "Beta": round(beta, 2),
            "Alpha": round(alpha, 2),
            f"Return {years}Y %": round(stock_annual_return * 100, 2),
            "Momentum Score 30D": round(mom_score, 2),
        })

    result_df = pd.DataFrame(result)
    result_df.set_index("Symbol", inplace=True)
    # adding last price
    price_df = pd.DataFrame(round(price,2))
    result_df["price"]=price_df.iloc[-1]
    # adding Quantity and Alocation
    result_df["No. Of Shares"]= df['Quantity']
    result_df["Value"]= result_df["No. Of Shares"] * result_df["price"]
    current_value = result_df["Value"].sum()
    
    invested_value =(df["Buy Price"] * df["Quantity"]).sum()
    result_df["Alocation %"]= round((result_df["Value"]/current_value)*100, 1)
    banchmark_total = banchmark_total.to_frame(name="Nifty")
    portfolio_total=pd.concat([portfolio_total,banchmark_total],axis= 1)
    Distribution_index =get_sector(name_list)
    result_df =pd.concat([Distribution_index,result_df],axis= 1)
    result_df=result_df.drop(["^NSEI"])

    return result_df, portfolio_total, invested_value, get_fundaments(name_list)

def get_sector(name_list):

    sector_data = []
    for tick in name_list:
        try:
            ticker = yf.Ticker(tick)
            sector = ticker.info.get('sector', 'N/A') 
            temp ={'Symbol': tick, 'Sector': sector}
            sector_data.append(temp)
        except Exception as e:
            print(e)

    sector_data_df =pd.DataFrame(sector_data)
    index_sector_data_df = sector_data_df.set_index('Symbol')

    return index_sector_data_df

def get_chart_data(price,Quantity):
    Quantity = pd.Series(Quantity)
    price_total = price.mul(Quantity,axis=1)
    price_total["Total"]= price_total.sum(axis=1,skipna= True)
    price_total =price_total.drop("^NSEI",axis=1)
    return price_total

def get_fundaments(name_list):
    fundaments_list = []
    new_entry = []
    info_list = ['marketCap', 'trailingPE', 'priceToBook', 'dividendYield', 'priceToSalesTrailing12Months', 'sector', 'averageAnalystRating', 'returnOnEquity' , 'revenueGrowth' , 'earningsGrowth']

    try:
        if "^NSEI" in name_list:
            name_list.remove("^NSEI")

        for name in name_list:
            ticker = yf.Ticker(name)
            current_stock_data = {"Symbol": name} 
            info_dict = ticker.info
            for metric_key in info_list:
                value = info_dict.get(metric_key, None)
                current_stock_data[metric_key] = value 

            fundaments_list.append(current_stock_data)
    except Exception as e:
        print(e)

    funda_df =pd.DataFrame(fundaments_list)
    funda_df["Market Cap"] =(funda_df["marketCap"]/10000000).round(0).astype(str) + " Cr"
    funda_df["P/E"] =funda_df["trailingPE"].round(0)
    funda_df["returnOnEquity"] = pd.to_numeric(funda_df["returnOnEquity"], errors='coerce')
    funda_df["RoC"] = funda_df["returnOnEquity"].apply(lambda x: f"{round(x * 100, 2)}%" if pd.notnull(x) else "N/A")
    funda_df["Dividend Yield"] =funda_df["dividendYield"].astype(str)+ "%"
    funda_df["Price to Sales"] =funda_df["priceToSalesTrailing12Months"].round(1)
    funda_df["Sales Growth"] =funda_df["revenueGrowth"].apply(lambda x: f"{round(x * 100, 2)}%" if pd.notnull(x) else "N/A")
    funda_df["Profit Growth"] =funda_df["earningsGrowth"].apply(lambda x: f"{round(x * 100, 2)}%" if pd.notnull(x) else "N/A")
    funda_df["Rating"] = funda_df["averageAnalystRating"]
    funda_df["Sector"] = funda_df["sector"]

    funda_df = funda_df.drop(columns= info_list, errors='ignore')
    return funda_df

get_data()
