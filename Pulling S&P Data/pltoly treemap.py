import yfinance as yf
import pandas as pd
import os

# File path for the cache
cache_file = 'market_cap_cache.csv'


# Function to get market capitalization from Yahoo Finance
def get_market_cap(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    market_cap = stock.info.get('marketCap', None)
    return market_cap


# Check if cache file exists
if os.path.exists(cache_file):
    # Load cached data if it exists
    cached_data = pd.read_csv(cache_file)
    print("Loaded market cap data from cache.")
else:
    # Read the S&P 500 data from the CSV file
    sp500_df = pd.read_csv('sp500_companies_industries.csv')

    # Initialize a list for storing market cap data
    treemap_data = []

    # Fetch the market cap and industries
    for index, row in sp500_df.iterrows():
        ticker = row['Ticker']
        company_name = row['Company']
        industry = row['Industry']
        market_cap = get_market_cap(ticker)

        if market_cap is not None:
            treemap_data.append({
                'Ticker': ticker,
                'Company': company_name,
                'Industry': industry,
                'MarketCap': market_cap
            })

    # Convert the data into a DataFrame
    cached_data = pd.DataFrame(treemap_data)

    # Save the data to CSV to use as cache
    cached_data.to_csv(cache_file, index=False)
    print("Market cap data fetched and cached.")

# Continue with the visualization
# Calculate total market cap per industry
industry_market_caps = cached_data.groupby('Industry')['MarketCap'].sum().reset_index()
industry_market_caps.columns = ['Industry', 'TotalMarketCap']

# Merge total market cap back into the main DataFrame
treemap_df = pd.merge(cached_data, industry_market_caps, on='Industry')

# Use Plotly for the treemap visualization
import plotly.express as px

# Create the treemap plot
fig = px.treemap(treemap_df,
                 path=['Industry', 'Company'],
                 values='MarketCap',
                 title='Market Capitalization Treemap for S&P 500 Industries and Companies',
                 color='MarketCap',
                 color_continuous_scale='Blues')

# Update hovertemplate for better information
fig.update_traces(hovertemplate=
                  '<b>%{label}</b><br>' +
                  'Market Cap: %{value:$.2s}<br>' +
                  '<extra>' +
                  'Industry Total Market Cap: %{customdata[0]:$.2s}<br>' +
                  'Company Market Cap: %{value:$.2s}' +
                  '</extra>')

# Show the treemap plot
fig.show()
