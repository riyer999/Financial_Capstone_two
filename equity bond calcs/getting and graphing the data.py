import yfinance as yf
import time
import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt



# Load NASDAQ tickers
file_path = '../us_official_nasdaq.csv'
nasdaq_df = pd.read_csv(file_path)
tickers = nasdaq_df['Ticker'].tolist()

# Initialize list to store Equity Bond values
equity_bonds = []
valid_tickers = []

# Loop through each ticker
for ticker in tickers:
    try:
        ystock = yf.Ticker(ticker)
        stock_info = ystock.info
        outstanding_shares = stock_info.get('sharesOutstanding')
        current_price = stock_info.get('currentPrice')

        income_statement = ystock.incomestmt
        pretax_income = income_statement.loc['Pretax Income', '2023']

        if outstanding_shares and current_price and not pretax_income.isnull().any():
            pretax_per_share = pretax_income / outstanding_shares
            equity_bond = (pretax_per_share / current_price) * 100
            equity_bonds.append(equity_bond.item())
            valid_tickers.append(ticker)

            print(f"{ticker}: Equity Bond = {equity_bond.item()}%")

        time.sleep(1)  # Regular delay
    except Exception as e:
        print(f"Error for {ticker}: {e}")
        if "429" in str(e):
            print("Rate limit hit. Waiting 60 seconds...")
            time.sleep(60)  # Wait longer if rate-limited
        continue

# Plot the distribution
plt.figure(figsize=(10, 5))
plt.hist(equity_bonds, bins=50, alpha=0.7, color='blue', edgecolor='black')
plt.xlabel("Equity Bond (%)")
plt.ylabel("Number of Companies")
plt.title("Distribution of Equity Bond Across NASDAQ Companies")
plt.grid(True)
plt.show()
