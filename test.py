import yfinance as yf
t = yf.Ticker("HDFCBANK.NS")
print(t.info)
print(t.info.get('trailingPE'))