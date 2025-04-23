import pandas as pd
import yfinance as yf
from collections import defaultdict
import time

# Load your CSV with a 'Ticker' column
sp500_df = pd.read_csv('sp500_company.csv')
tickers = sp500_df['Ticker'].dropna().unique()

# Initialize totals
total_pretax = defaultdict(float)
total_market_cap = defaultdict(float)
years = ['2021', '2022', '2023', '2024']

# Function to handle rate limiting
def safe_fetch_ticker(ticker, retries=5, delay=5):
    for attempt in range(retries):
        try:
            stock = yf.Ticker(ticker)
            return stock
        except Exception as e:
            if "Too Many Requests" in str(e):
                print(f"Rate limit hit for {ticker}. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                print(f"Error fetching {ticker}: {e}")
                break
    return None

# Loop through S&P 500 companies
for ticker in tickers:
    try:
        # Fetch stock data with rate limit handling
        stock = safe_fetch_ticker(ticker)
        if not stock:
            print(f"Skipping {ticker} due to repeated errors.")
            continue

        income_statement = stock.financials  # Get the full financials
        market_cap = stock.info.get('marketCap', None)

        # Debugging: Check the structure of the income statement
        print(f"DEBUG: Income statement for {ticker}:")
        print(income_statement.head())  # Print first few rows to see the available data

        if income_statement.empty or market_cap is None:
            print(f"DEBUG: No data available for {ticker}")
            continue

        # Loop over each year and check if 'Pretax Income' is available
        for year in years:
            year_key = f'{year}-12-31'
            if year_key in income_statement.columns:
                try:
                    # Fetch 'Pretax Income' for the given year
                    if 'Pretax Income' in income_statement.index:
                        pretax_income = income_statement.loc['Pretax Income', year_key]
                        if pd.notna(pretax_income):  # Ensure no NaN value
                            total_pretax[year] += pretax_income
                            total_market_cap[year] += market_cap
                    else:
                        print(f"DEBUG: 'Pretax Income' not found for {ticker} in {year}")
                        continue
                except KeyError:
                    print(f"DEBUG: KeyError when processing {ticker} for {year}")
                    continue  # Skip if 'Pretax Income' is not found
        time.sleep(1)  # Add delay to avoid hitting rate limits too quickly
    except Exception as e:
        print(f"Error processing {ticker}: {e}")
        continue

# Calculate and store average equity bond yield
average_equity_yields = {}
for year in years:
    if total_market_cap[year] > 0:
        average_yield = (total_pretax[year] / total_market_cap[year]) * 100
        average_equity_yields[year] = round(average_yield, 2)

print("Average Equity Bond Yields for S&P 500:")
print(average_equity_yields)
