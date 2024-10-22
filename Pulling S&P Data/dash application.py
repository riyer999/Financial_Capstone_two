import yfinance as yf
import pandas as pd
import os
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

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

# Group by Industry to calculate total market cap per industry
industry_market_caps = cached_data.groupby('Industry')['MarketCap'].sum().reset_index()
industry_market_caps.columns = ['Industry', 'TotalMarketCap']

# Merge total market cap back into the main DataFrame
treemap_df = pd.merge(cached_data, industry_market_caps, on='Industry')

# Initialize Dash application
app = Dash(__name__)

# Layout of the Dash application
app.layout = html.Div([
    html.H1("S&P 500 Market Capitalization Treemap"),
    dcc.Graph(
        id='treemap',
        config={'displayModeBar': False}  # Hide mode bar for a cleaner look
    ),
    html.Div(id='company-details', style={'margin-top': '20px'}),
    dcc.Graph(id='industry-pie-chart', style={'margin-top': '20px'})
])

# Create the treemap plot
@app.callback(
    Output('treemap', 'figure'),
    Input('treemap', 'id')  # Dummy input to trigger the initial render
)
def update_treemap(_):
    # Create the treemap plot
    fig = px.treemap(treemap_df,
                     path=['Industry', 'Company'],
                     values='MarketCap',
                     title='Market Capitalization Treemap for S&P 500 Industries and Companies',
                     color='MarketCap',
                     color_continuous_scale='Blues',
                     hover_data=['MarketCap'])

    # Update hovertemplate for better information
    fig.update_traces(hovertemplate=
                      '<b>%{label}</b><br>' +
                      'Market Cap: %{value:$.2s}<br>' +
                      '<extra>' +
                      'Industry Total Market Cap: %{customdata[0]:$.2s}<br>' +
                      'Company Market Cap: %{value:$.2s}' +
                      '</extra>')
    return fig

# Callback for displaying company details and pie chart when a company is clicked
@app.callback(
    Output('company-details', 'children'),
    Output('industry-pie-chart', 'figure'),
    Input('treemap', 'clickData')
)
def display_company_details(clickData):
    if clickData is None:
        return "Click on a company to see details.", {}  # Default message and empty chart

    # Extract company name from click data
    company_name = clickData['points'][0]['label']
    selected_company = cached_data[cached_data['Company'] == company_name].iloc[0]

    # Get details for the selected company
    ticker = selected_company['Ticker']
    market_cap = selected_company['MarketCap']
    industry = selected_company['Industry']

    # Prepare details to display
    details = [
        html.H4(f"Company: {company_name}"),
        html.P(f"Ticker: {ticker}"),
        html.P(f"Industry: {industry}"),
        html.P(f"Market Cap: ${market_cap:,.2f}")
    ]

    # Create a pie chart for the industry's market cap distribution
    industry_data = treemap_df[treemap_df['Industry'] == industry]

    pie_fig = px.pie(industry_data,
                     values='MarketCap',
                     names='Company',
                     title=f'Market Cap Distribution in {industry}',
                     hover_data=['MarketCap'])

    return details, pie_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
