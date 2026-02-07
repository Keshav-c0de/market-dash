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
    banchmark_total = banchmark_total.to_frame(name="Price")

    
    return result_df, portfolio_total, invested_value, banchmark_total

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


def get_chart_data(price,Quantity):
    Quantity = pd.Series(Quantity)
    price_total = price.mul(Quantity,axis=1)
    price_total["Total"]= price_total.sum(axis=1,skipna= True)
    price_total =price_total.drop("^NSEI",axis=1)
    return price_total

get_data()