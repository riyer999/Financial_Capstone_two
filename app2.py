import yfinance as yf
import pandas as pd
import os
import pickle
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

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
    st.write("Loaded market cap data from cache.")
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
    st.write("Market cap data fetched and cached.")

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

    return fig


# Load financial data for a given company and year
def load_data(ticker, year='2023'):
    with open('allData.pkl', 'rb') as file:
        allData = pickle.load(file)

    income_statement = allData[ticker]['income_statement']

    # List of keys to extract from the income statement
    keys = [
        'Total Unusual Items',
        'Total Unusual Items Excluding Goodwill',
        'Net Interest Income',
        'Interest Expense',
        'Interest Income',
        'Normalized Income',
        'Total Operating Income As Reported',
        'Basic Average Shares',
        'Net Income Common Stockholders',
        'Net Income',
        'Minority Interests',
        'Net Income Including Noncontrolling Interests',
        'Net Income Continuous Operations',
        'Tax Provision',
        'Pretax Income',
        'Other Income Expense',
        'Impairment Of Capital Assets',
        'Net Non Operating Interest Income Expense',
        'Interest Expense Non Operating',
        'Operating Income',
        'Operating Expense',
        'Other Operating Expenses',
        'Selling General And Administration',
        'General And Administrative Expense',
        'Gross Profit',
        'Cost Of Revenue',
        'Total Revenue',
        'Operating Revenue'
    ]

    variable_names = {key.replace(" ", "_"): income_statement.loc[key, year].item() for key in keys}
    return variable_names


# Streamlit layout
st.title("S&P 500 Market Capitalization Treemap")  # Title for the page
fig = create_treemap()
st.plotly_chart(fig)  # Treemap component

# Interactive selection of company
selected_company = st.selectbox("Select a company from the treemap:", options=treemap_df['Company'].unique())

if selected_company:
    # Normalize the company name for matching
    company_name_normalized = selected_company.strip().lower()
    matched_tickers = treemap_df[treemap_df['Company'].str.strip().str.lower() == company_name_normalized]['Ticker']

    if not matched_tickers.empty:
        ticker = matched_tickers.values[0]

        # Load financial data for the selected company
        financial_metrics = load_data(ticker)

        if financial_metrics:
            # Extract financial metrics
            # total_revenue = financial_metrics.get('Total_Revenue', 0) / 1e9
            # gross_profit_value = financial_metrics.get('Gross_Profit', 0) / 1e9
            # cost_revenue = financial_metrics.get('Cost_Of_Revenue', 0) / 1e9
            # operating_income = financial_metrics.get('Operating_Income', 0) / 1e9
            # operating_expense = financial_metrics.get('Operating_Expense', 0) / 1e9
            # net_income = financial_metrics.get('Net_Income', 0) / 1e9
            total_revenue = financial_metrics['Total_Revenue'] / 1000000000
            gross_profit_value = financial_metrics['Gross_Profit'] / 1000000000
            cost_revenue = financial_metrics['Cost_Of_Revenue'] / 1000000000
            operating_income = financial_metrics['Operating_Income'] / 1000000000
            operating_expense = financial_metrics['Operating_Expense'] / 1000000000
            tax_provision = financial_metrics['Tax_Provision'] / 1000000000
            sga = financial_metrics['Selling_General_And_Administration'] / 1000000000
            other = financial_metrics['Other_Income_Expense'] / 1000000000
            net_income = financial_metrics['Net_Income'] / 1000000000
            ga = financial_metrics['General_And_Administrative_Expense'] / 1000000000
            other_operating_expenses = financial_metrics['Other_Operating_Expenses'] / 1000000000

            # Create the Sankey diagram
            label = ['Revenue',  # this one is fine
                     'Gross Profit',  # this one is also fine
                     'Cost of Revenues',
                     'Operating Profit',
                     'Operating Expenses',
                     'Net Profit',
                     'Tax',
                     'Other',
                     'SG&A',
                     'Other Expenses'
                     ]

            # Data
            source = [0, 0, 1, 1, 3, 3, 3, 4, 4]
            target = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            # gross profit, cost of revenues,
            value = [gross_profit_value, cost_revenue, operating_income, operating_expense, net_income, tax_provision,
                     other, sga, other_operating_expenses]

            link = dict(source=source, target=target, value=value)
            node = dict(label=label, pad=35, thickness=20)
            fig_sankey = go.Figure(data=[go.Sankey(link=link, node=node)])

            fig_sankey.update_layout(
                title="<span style='font-size:36px;color:steelblue;'><b>Income Statement for " + selected_company + "</b></span>",
                font=dict(size=10, color='black'),
                paper_bgcolor='white'
            )
            if total_revenue > 0:
                fig.add_annotation(
                    dict(font=dict(color="steelblue", size=12), x=0.08, y=0.99, showarrow=False, text='<b>Revenue</b>'))
                fig.add_annotation(dict(font=dict(color="steelblue", size=12), x=0.08, y=0.96, showarrow=False,
                                        text=f'<b>${total_revenue:.1f}B</b>'))

            # Gross Profit
            if gross_profit_value > 0:
                fig.add_annotation(dict(font=dict(color="green", size=12), x=0.315, y=0.99, showarrow=False,
                                        text='<b>Gross Profit</b>'))
                fig.add_annotation(dict(font=dict(color="green", size=12), x=0.33, y=0.96, showarrow=False,
                                        text=f'<b>${gross_profit_value:.1f}B</b>'))

            # Operating Profit
            if operating_income > 0:
                fig.add_annotation(dict(font=dict(color="green", size=12), x=0.61, y=1.05, showarrow=False,
                                        text='<b>Operating Profit</b>'))
                fig.add_annotation(dict(font=dict(color="green", size=12), x=0.61, y=1.02, showarrow=False,
                                        text=f'<b>${operating_income:.1f}B</b>'))

            # Net Profit
            if net_income > 0:
                fig.add_annotation(
                    dict(font=dict(color="green", size=12), x=0.95, y=1.05, showarrow=False, text='<b>Net Profit</b>'))
                fig.add_annotation(dict(font=dict(color="green", size=12), x=0.94, y=1, showarrow=False,
                                        text=f'<b>${net_income:.1f}B</b>'))

            # Tax
            if tax_provision > 0:
                fig.add_annotation(
                    dict(font=dict(color="maroon", size=12), x=0.93, y=0.9, showarrow=False, text='<b>Tax</b>'))
                fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.935, y=0.85, showarrow=False,
                                        text=f'<b>${tax_provision:.1f}B</b>'))

            # Other
            if other > 0:
                fig.add_annotation(
                    dict(font=dict(color="maroon", size=12), x=0.935, y=0.75, showarrow=False, text='<b>Other</b>'))
                fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.935, y=0.70, showarrow=False,
                                        text=f'<b>${other:.1f}B</b>'))

            # SG&A
            if sga > 0:
                fig.add_annotation(
                    dict(font=dict(color="maroon", size=12), x=0.93, y=0.58, showarrow=False, text='<b>SG&A</b>'))
                fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.93, y=0.52, showarrow=False,
                                        text=f'<b>${sga:.1f}B</b>'))

            # Other Operating Expenses
            if other_operating_expenses > 0:
                fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.95, y=0.40, showarrow=False,
                                        text='<b>Other<br>Operating<br>Expenses</b>'))
                fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.935, y=0.26, showarrow=False,
                                        text=f'<b>${other_operating_expenses:.1f}B</b>'))

            # Operating Expenses
            if operating_expense > 0:
                fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.59, y=0.41, showarrow=False,
                                        text='<b>Operating<br>Expenses</b>'))
                fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.59, y=0.34, showarrow=False,
                                        text=f'<b>${operating_expense:.1f}B</b>'))

            # Cost of Revenues
            if cost_revenue > 0:
                fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.34, y=0.08, showarrow=False,
                                        text='<b>Cost of<br>Revenues</b>'))
                fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.34, y=0.05, showarrow=False,
                                        text=f'<b>${cost_revenue:.1f}B</b>'))

            st.plotly_chart(fig_sankey)
