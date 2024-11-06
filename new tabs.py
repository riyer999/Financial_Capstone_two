import yfinance as yf
import pandas as pd
import os
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pickle


# Initialize the Dash application
app = Dash(__name__, suppress_callback_exceptions=True)
server = app.server

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


# Calculate total market cap per industry
industry_market_caps = cached_data.groupby('Industry')['MarketCap'].sum().reset_index()
industry_market_caps.columns = ['Industry', 'TotalMarketCap']

# Merge total market cap back into the main DataFrame
treemap_df = pd.merge(cached_data, industry_market_caps, on='Industry')

# Create the treemap plot using Plotly Express
def create_treemap():
    fig = px.treemap(treemap_df,
                     path=['Industry', 'Company'],
                     values='MarketCap',
                     color='MarketCap',
                     color_continuous_scale='Blues')

    return fig

# Define the layout of the Dash application
app.layout = html.Div([
    dcc.Location(id='url', refresh=True),  # URL component for redirection
    html.Div(id='page-content'),           # Dynamic content based on the URL
])

# Main page layout with the treemap
main_page_layout = html.Div([
    html.H1("S&P 500 Market Capitalization Treemap"),  # Title for the page
    dcc.Graph(id='treemap', figure=create_treemap(), clickData=None),  # Treemap component
])

# Detailed page layout with company information (displayed when clicking on a company)
def get_company_details(company_name):
    # Assuming the company data is available in your DataFrame
    company_data = treemap_df[treemap_df['Company'] == company_name]
    # Add more details you want to show here, e.g., market cap, financials
    return html.Div([
        html.H2(f"Details for {company_name}"),
        html.P(f"Market Cap: {company_data['MarketCap'].values[0]}"),
        # You can add more financial data or charts here
        html.A(html.Button("Back to Treemap", id="back-button"), href='/')
    ])

# Callback to update the page layout based on URL
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    # Display the main page layout
    if pathname == '/' or pathname == '':
        return main_page_layout
    # Display the company details page when a company is clicked
    elif pathname.startswith('/company/'):
        company_name = pathname.split('/')[-1]
        return get_company_details(company_name)

# Callback to handle item clicks in the treemap and redirect to a new URL
@app.callback(
    Output('url', 'pathname'),
    Input('treemap', 'clickData')
)
def update_treemap(click_data):
    # Check if an item was clicked
    if click_data:
        company_name = click_data['points'][0]['label']
        # Navigate to the company detail page
        return f'/company/{company_name}'
    return '/'  # Stay on the main page if nothing is clicked

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
