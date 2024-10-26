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

    variable_names = {}
    for key in keys:
        variable_name = key.replace(" ", "_")
        # Try to extract the value, return 0 if key doesn't exist
        try:
            variable_names[variable_name] = abs(income_statement.loc[key, year].item())
        except KeyError:
            variable_names[variable_name] = 0

    return variable_names  # Return the dictionary with variable names and values

# Define the layout of the Dash application
app.layout = html.Div([
    html.H1("S&P 500 Market Capitalization Treemap"),  # Title for the page
    html.Div(id='treemap-area', children=[
        dcc.Graph(id='treemap', figure=create_treemap()),  # Treemap component
        dcc.Graph(id='company-graphic', style={'display': 'none', 'height': '500px'})  # Initially hidden
    ])
])

# Callback to update the graphic based on treemap click
@app.callback(
    [Output('company-graphic', 'figure'), Output('company-graphic', 'style')],
    [Input('treemap', 'clickData')]
)
def update_graphic(clickData):
    if clickData is not None:
        company_name = clickData['points'][0]['label']

        # Normalize the company name for matching
        company_name_normalized = company_name.strip().lower()

        treemap_df['Normalized_Company'] = treemap_df['Company'].str.strip().str.lower()
        matched_tickers = treemap_df[treemap_df['Normalized_Company'] == company_name_normalized]['Ticker']

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
                ###################################################
                color_link = ['#000000', '#FFFF00', '#1CE6FF', '#FF34FF', '#FF4A46',
                              '#008941', '#006FA6', '#A30059', '#FFDBE5', '#7A4900',
                              '#0000A6', '#63FFAC', '#B79762', '#004D43', '#8FB0FF',
                              '#997D87', '#5A0007', '#809693', '#FEFFE6', '#1B4400',
                              '#4FC601', '#3B5DFF', '#4A3B53', '#FF2F80', '#61615A',
                              '#BA0900', '#6B7900', '#00C2A0', '#FFAA92', '#FF90C9',
                              '#B903AA', '#D16100', '#DDEFFF', '#000035', '#7B4F4B',
                              '#A1C299', '#300018', '#0AA6D8', '#013349', '#00846F',
                              '#372101', '#FFB500', '#C2FFED', '#A079BF', '#CC0744',
                              '#C0B9B2', '#C2FF99', '#001E09', '#00489C', '#6F0062',
                              '#0CBD66', '#EEC3FF', '#456D75', '#B77B68', '#7A87A1',
                              '#788D66', '#885578', '#FAD09F', '#FF8A9A', '#D157A0',
                              '#BEC459', '#456648', '#0086ED', '#886F4C', '#34362D',
                              '#B4A8BD', '#00A6AA', '#452C2C', '#636375', '#A3C8C9',
                              '#FF913F', '#938A81', '#575329', '#00FECF', '#B05B6F',
                              '#8CD0FF', '#3B9700', '#04F757', '#C8A1A1', '#1E6E00',
                              '#7900D7', '#A77500', '#6367A9', '#A05837', '#6B002C',
                              '#772600', '#D790FF', '#9B9700', '#549E79', '#FFF69F',
                              '#201625', '#72418F', '#BC23FF', '#99ADC0', '#3A2465',
                              '#922329', '#5B4534', '#FDE8DC', '#404E55', '#0089A3',
                              '#CB7E98', '#A4E804', '#324E72', '#6A3A4C'
                              ]

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

                color_for_nodes = ['steelblue', 'green', 'red', 'green', 'red', 'green', 'red', 'red',
                                   'red', 'red']

                color_for_links = ['lightgreen', 'PaleVioletRed', 'lightgreen', 'PaleVioletRed',
                                   'lightgreen',
                                   'PaleVioletRed', 'PaleVioletRed', 'PaleVioletRed', 'PaleVioletRed']

                # Data
                source = [0, 0, 1, 1, 3, 3, 3, 4, 4]
                target = [1, 2, 3, 4, 5, 6, 7, 8, 9]
                # gross profit, cost of revenues,
                value = [gross_profit_value, cost_revenue, operating_income, operating_expense, net_income,
                         tax_provision, other, sga, other_operating_expenses]

                link = dict(source=source, target=target, value=value, color=color_link)
                node = dict(label=label, pad=35, thickness=20)
                data = go.Sankey(link=link, node=node)

                x = [0.1, 0.35, 0.35, 0.6,
                     0.6, 0.85, 0.85, 0.85, 0.85, 0.85]
                y = [0.40, 0.25, 0.70, 0.1,
                     0.45, 0.0, 0.15, 0.30, 0.45, 0.60]
                x = [.001 if v == 0 else .999 if v == 1 else v for v in x]
                y = [.001 if v == 0 else .999 if v == 1 else v for v in y]

                fig = go.Figure(data=[go.Sankey(

                    textfont=dict(color="rgba(0,0,0,0)", size=1),
                    node=dict(
                        pad=35,
                        line=dict(color="white", width=1),
                        label=label,
                        x=x,
                        y=y
                    ),
                    link=dict(
                        source=source,
                        target=target,
                        value=value
                    ))])

                fig.update_layout(
                    hovermode='x',
                    title=f"<span style='font-size:36px;color:steelblue;'><b>{company_name}KO FY23 Income Statement</b></span>",
                    font=dict(size=10, color='white'),
                    paper_bgcolor='#F8F8FF'
                )

                fig.update_traces(node_color=color_for_nodes,
                                  link_color=color_for_links)

                # x = [   0.1, 0.35, 0.35,  0.6, 0.6, 0.6,
                #      0.6, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85]
                # y = [  0.40, 0.25, 0.70, 0.1, 0.40,
                #     0.70, 0.90, 0.0, 0.15, 0.30, 0.45, 0.60, 0.75]
                # Revenue

                # Revenue
                if total_revenue > 0:
                    fig.add_annotation(dict(font=dict(color="steelblue", size=12), x=0.08, y=0.99, showarrow=False,
                                            text='<b>Revenue</b>'))
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
                    fig.add_annotation(dict(font=dict(color="green", size=12), x=0.95, y=1.05, showarrow=False,
                                            text='<b>Net Profit</b>'))
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

                fig.show()
                return fig, {'display': 'block'}  # Show the Sankey diagram
        else:
            return go.Figure(), {'display': 'none'}  # Return empty figure if no company is found
    else:
        return go.Figure(), {'display': 'none'}  # Return empty figure if no company clicked

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
