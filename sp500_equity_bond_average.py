import pandas as pd
import yfinance as yf
from collections import defaultdict
import time

# Load your CSV with 'Ticker' and 'Industry' columns
sp500_df = pd.read_csv('sp500_company.csv')
tickers = sp500_df['Ticker'].dropna().unique()
industries = sp500_df['Industry'].dropna().unique()
years = ['2021', '2022', '2023', '2024']

# Initialize totals by industry and year
industry_pretax = {industry: defaultdict(float) for industry in industries}
industry_market_cap = {industry: defaultdict(float) for industry in industries}

# Function to handle rate limiting
def safe_fetch_ticker(ticker, retries=5, delay=5):
    for attempt in range(retries):
        try:
            return yf.Ticker(ticker)
        except Exception as e:
            if "Too Many Requests" in str(e):
                print(f"Rate limit hit for {ticker}. Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= 2
            else:
                print(f"Error fetching {ticker}: {e}")
                break
    return None

# Loop through companies
for _, row in sp500_df.iterrows():
    ticker = row['Ticker']
    industry = row['Industry']

    try:
        stock = safe_fetch_ticker(ticker)
        if not stock:
            print(f"Skipping {ticker} due to repeated errors.")
            continue

        income_statement = stock.financials
        market_cap = stock.info.get('marketCap', None)

        if income_statement.empty or market_cap is None:
            continue

        for year in years:
            year_key = f'{year}-12-31'
            if year_key in income_statement.columns and 'Pretax Income' in income_statement.index:
                try:
                    pretax_income = income_statement.loc['Pretax Income', year_key]
                    if pd.notna(pretax_income):
                        industry_pretax[industry][year] += pretax_income
                        industry_market_cap[industry][year] += market_cap
                except KeyError:
                    continue
        time.sleep(1)
    except Exception as e:
        print(f"Error processing {ticker}: {e}")
        continue

# Calculate average equity bond yield by industry
industry_equity_yields = {
    industry: {
        year: round((industry_pretax[industry][year] / industry_market_cap[industry][year]) * 100, 2)
        for year in years if industry_market_cap[industry][year] > 0
    }
    for industry in industries
}

print("Average Equity Bond Yields by Industry:")
for industry, data in industry_equity_yields.items():
    print(industry, data)
