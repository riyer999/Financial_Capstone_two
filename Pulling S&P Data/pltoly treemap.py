# Import yfinance for fetching financial data, pandas for handling dataframes, and os for file handling operations
import yfinance as yf
import pandas as pd
import os

# Define the path to the CSV file that will store cached market cap data
cache_file = '../market_cap_cache.csv'


# Define a function that takes a stock ticker symbol as input and returns its market capitalization
def get_market_cap(ticker_symbol):
    # Use yfinance to fetch the stock information for the given ticker symbol
    stock = yf.Ticker(ticker_symbol)
    # Extract the market capitalization information from the stock data
    # Use 'None' as a default value in case the market cap is missing
    market_cap = stock.info.get('marketCap', None)
    # Return the market capitalization
    return market_cap


# Check if the cache file (CSV) exists in the file system
if os.path.exists(cache_file):
    # If the cache file exists, load the cached market cap data from the CSV file into a pandas DataFrame
    cached_data = pd.read_csv(cache_file)
    print("Loaded market cap data from cache.")  # Inform the user that cached data is being used
else:
    # If the cache file does not exist, load the S&P 500 data from a separate CSV file containing tickers and industries
    sp500_df = pd.read_csv('../sp500_companies_industries.csv')

    # Initialize an empty list to store market cap data as dictionaries for each company
    treemap_data = []

    # Iterate over each row in the S&P 500 dataframe to fetch data for each company
    for index, row in sp500_df.iterrows():
        # Extract the ticker symbol, company name, and industry from the current row
        ticker = row['Ticker']
        company_name = row['Company']
        industry = row['Industry']

        # Fetch the market capitalization for the current ticker using the get_market_cap function
        market_cap = get_market_cap(ticker)

        # If the market cap is successfully fetched (i.e., it is not None)
        if market_cap is not None:
            # Append the company data (ticker, company name, industry, and market cap) to the treemap_data list
            treemap_data.append({
                'Ticker': ticker,
                'Company': company_name,
                'Industry': industry,
                'MarketCap': market_cap
            })

    # Convert the list of dictionaries into a pandas DataFrame for easier handling and analysis
    cached_data = pd.DataFrame(treemap_data)

    # Save the newly fetched data to a CSV file to serve as a cache for future runs
    cached_data.to_csv(cache_file, index=False)
    print("Market cap data fetched and cached.")  # Inform the user that data was fetched and saved to cache

# Now, we move on to the visualization part
# Group the data by 'Industry' and calculate the total market cap for each industry
industry_market_caps = cached_data.groupby('Industry')['MarketCap'].sum().reset_index()

# Rename the columns for clarity ('Industry' and 'TotalMarketCap')
industry_market_caps.columns = ['Industry', 'TotalMarketCap']

# Merge the original company-level data with the industry-level market cap totals
# This will allow us to display both individual companies and their industries in the visualization
treemap_df = pd.merge(cached_data, industry_market_caps, on='Industry')

# Import Plotly Express for easy plotting of the treemap
import plotly.express as px

# Create the treemap plot using Plotly Express
# 'path' defines the hierarchical structure (Industry -> Company)
# 'values' is the size of each block in the treemap, which is determined by the company's market capitalization
# 'color' assigns colors based on the market capitalization to create a gradient
# 'color_continuous_scale' defines the color scale to use (in this case, 'Blues')
fig = px.treemap(treemap_df,
                 path=['Industry', 'Company'],
                 values='MarketCap',
                 title='Market Capitalization Treemap for S&P 500 Industries and Companies',
                 color='MarketCap',
                 color_continuous_scale='Blues')

# Update the hover template to display more detailed information when hovering over each block in the treemap
# %{label} is the name of the company or industry
# %{value} is the market capitalization value, formatted as currency
# The extra field displays both industry and company market cap
fig.update_traces(hovertemplate=
                  '<b>%{label}</b><br>' +  # Display the company/industry name in bold
                  'Market Cap: %{value:$.2s}<br>' +  # Show the market cap, formatted with two significant digits
                  '<extra>' +
                  'Industry Total Market Cap: %{customdata[0]:$.2s}<br>' +  # Show the total market cap of the industry
                  'Company Market Cap: %{value:$.2s}' +  # Show the market cap of the individual company
                  '</extra>')

# Finally, display the treemap plot
fig.show()
