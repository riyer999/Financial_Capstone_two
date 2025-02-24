import time
import yfinance as yf

ticker = "AAPL"
stock = yf.Ticker(ticker)

# Add a delay before making the request
time.sleep(2)

market_cap = stock.info.get("marketCap", "N/A")
print(f"Apple's Market Cap: {market_cap:,}")
import time
import yfinance as yf

ticker = "AAPL"
stock = yf.Ticker(ticker)

# Add a delay before making the request
time.sleep(2)

market_cap = stock.info.get("marketCap", "N/A")
print(f"Apple's Market Cap: {market_cap:,}")
