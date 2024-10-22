import yfinance as yf
import pandas as pd
import os
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pickle

# Initialize the Dash application
app = Dash(__name__, suppress_callback_exceptions=True)

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
    return fig

# Load the financial data for the selected company
def load_data(ticker, year='2023'):
    with open('allData.pkl', 'rb') as file:
        allData = pickle.load(file)

    income_statement = allData[ticker]['income_statement']

    # List of keys to extract from the income statement
    keys = [
        'Gross Profit',
        'Cost Of Revenue',
        'Total Revenue',
        'Operating Expense'
    ]

    # Create a dictionary to hold variable names and their corresponding values
    variable_names = {key.replace(" ", "_"): income_statement.loc[key, year].item() for key in keys}

    return variable_names  # Return the dictionary with variable names and values

# Define the layout of the Dash application
# Define the layout of the Dash application
app.layout = html.Div([
    html.H1("S&P 500 Market Capitalization Treemap"),  # Title for the page
    html.Div(id='treemap-area', children=[
        dcc.Graph(id='treemap', figure=create_treemap()),  # Your treemap component
        dcc.Graph(id='company-graphic', style={'display': 'none', 'height': '300px'})  # Initially hidden
    ])
])


@app.callback(
    [Output('company-graphic', 'figure'), Output('company-graphic', 'style')],
    [Input('treemap', 'clickData')]
)
def update_graphic(clickData):
    if clickData is not None:
        company_name = clickData['points'][0]['label']

        # Normalize the case and strip whitespace
        company_name_normalized = company_name.strip().lower()

        # Print for debugging
        print(f"Clicked company: {company_name_normalized}")

        # Normalize the case and strip whitespace for comparison
        treemap_df['Normalized_Company'] = treemap_df['Company'].str.strip().str.lower()

        # Find the ticker using a case-insensitive comparison
        matched_tickers = treemap_df[treemap_df['Normalized_Company'] == company_name_normalized]['Ticker']

        # Print matched tickers for debugging
        print(f"Matched tickers for {company_name_normalized}: {matched_tickers.values}")

        if not matched_tickers.empty:
            ticker = matched_tickers.values[0]

            # Load financial data for the selected company
            financial_metrics = load_data(ticker)

            # Prepare data for the bar chart
            metrics = [
                financial_metrics['Gross_Profit'] / 1e9,  # Convert to billions
                financial_metrics['Cost_Of_Revenue'] / 1e9,
                financial_metrics['Total_Revenue'] / 1e9,
                financial_metrics['Operating_Expense'] / 1e9
            ]
            metric_labels = ['Gross Profit', 'Cost of Revenue', 'Total Revenue', 'Operating Expenses']

            # Create a bar chart using Plotly
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=metric_labels,
                y=metrics,
                marker_color=['blue', 'red', 'green', 'orange'],
                text=[f'{metric:.2f}B' for metric in metrics],
                textposition='auto'
            ))

            # Customize layout
            fig.update_layout(
                title=f"Financial Metrics for {company_name.title()} in 2023",
                xaxis_title="Metrics",
                yaxis_title="Amount (in Billions)",
                showlegend=False,
                height=300,  # Ensure height fits well over the treemap
                margin=dict(l=0, r=0, t=30, b=0)  # Remove extra margins if needed
            )

            # Return the figure and style to show the graphic
            return fig, {'display': 'block'}  # Ensure this is correctly set
        else:
            print(f"No matched tickers for: {company_name_normalized}. Skipping...")
            return {}, {'display': 'none'}  # Hide the graphic if the ticker is not found
    else:
        return {}, {'display': 'none'}  # Hide the graphic if no company is clicked

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
