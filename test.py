import yfinance as yf

# Replace with your target ticker
ticker = yf.Ticker("AAPL")

# Get company info
info = ticker.info

# Print the business summary
print(info["longBusinessSummary"])
