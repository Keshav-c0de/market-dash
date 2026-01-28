import yfinance as yf
import pandas as pd


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
    daily_returns =price.pct_change()
    df_stock =pd.DataFrame(daily_returns)
    df_stock =df_stock.dropna()
    banchmark = df_stock["^NSEI"]
    portfolio = df_stock.drop(columns=["^NSEI"])

    # Calculations
    variance = banchmark.var()
    for stocks in portfolio.columns:
        stock_data = portfolio[stocks]

        # Calculate beta
        covariance = stock_data.cov(banchmark)
        beta =(covariance/variance)

        # Annual Return Calculation
        stock_annual_return = stock_data.mean() * 252

        # Calculate alpha
        expected_return = RISK_FREE_RATE + beta * (market_annual_return - RISK_FREE_RATE)
        alpha = stock_annual_return - expected_return

        result.append({
            "Symbol": stocks,
            "Beta": round(beta, 2),
            "Alpha": round(alpha, 2),
            "Return 1Y %": round(stock_annual_return * 100, 2)
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
    
    return result_df, current_value, invested_value, banchmark

def get_sector():
    df = pd.read_csv("portfolio.csv")
    name_list = df['Symbol'].tolist()

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

get_sector()