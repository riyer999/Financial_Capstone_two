import yfinance as yf
import pandas as pd
import os
from dash import Dash, dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Step 1: Read the file into a DataFrame
file_path = 'us_official_nasdaq.csv'  # Replace with the path to your file
nasdaq_df = pd.read_csv(file_path)
nasdaq_df = pd.read_csv(file_path, dtype={'MarketCap': float}, low_memory=False)

def get_market_cap(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    market_cap = stock.info.get('marketCap', None)
    return market_cap

def load_data(ticker, years=['2020', '2021', '2022', '2023', '2024']):
    # Fetch the data dynamically using yfinance
    ystock = yf.Ticker(ticker)

    # Fetch the financial data
    income_statement = ystock.incomestmt
    print(income_statement)
    balance_sheet = ystock.balance_sheet
    cashflow_statement = ystock.cashflow  # This fetches the cash flow statement

    # Fetch the stock's information (including shares outstanding)
    stock_info = ystock.info
    outstanding_shares = stock_info.get('sharesOutstanding')
    #print(f"Outstanding Shares: {outstanding_shares}")
    current_price = stock_info.get('currentPrice')
    #print(f"Current Stock Price: ${current_price}")

    # List of keys to extract from the income statement
    income_statement_keys = [
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
        'Research And Development',
        'General And Administrative Expense',
        'Gross Profit',
        'Cost Of Revenue',
        'Total Revenue',
        'Operating Revenue'
        'Pretax Income'
    ]

    balance_sheet_keys = [
        'Total Assets',
        'Current Assets',
        'Cash Cash Equivalents And Short Term Investments',
        'Cash And Cash Equivalents',
        'Other Short Term Investments',
        'Receivables',
        'Inventory',
        'Raw Materials',
        'Finished Goods',
        'Other Inventories',
        'Prepaid Assets',
        'Other Current Assets',
        #
        'Total Non Current Assets',
        'Net PPE',
        'Goodwill And Other Intangible Assets',
        'Goodwill',
        'Other Intangible Assets',
        'Investments And Advances',
        'Long Term Equity Investment',
        'Other Investments',
        'Non Current Accounts Receivable',
        'Non Current Note Receivables',
        'Non Current Deferred Assets',
        'Defined Pension Benefit',
        'Other Non Current Assets',
        #
        'Total Liabilities Net Minority Interest',
        'Current Liabilities',
        'Payables And Accrued Expenses',
        'Pensionand Other Post Retirement Benefit Plans ...',
        'Current Debt And Capital Lease Obligation',
        'Other Current Liabilities',
        'Total Non Current Liabilities Net Minority Interest',
        'Long Term Debt And Capital Lease Obligation',
        'Non Current Deferred Liabilities',
        'Other Non Current Liabilities',
        #
        'Total Equity Gross Minority Interest',
        #
        'Stockholders Equity',
        'Capital Stock',
        'Additional Paid in Capital',
        'Retained Earnings',
        'Treasury Stock',
        'Gains Losses Not Affecting Retained Earnings',
        'Minority Interest',
    ]
    cashflow_statement_keys = {
        'Operating Cash Flow',
        'Issuance Of Debt',
        'Capital Expenditure',
        'Repayment Of Debt',
        'Repurchase Of Capital Stock',
    }

    variable_names = {}
    # loop through the years and each key for the income statement
    for year in years:
        for key in income_statement_keys:
            variable_name = f"{key.replace(' ', '_')}_{year}"  # Unique variable for each year
            try:
                value = income_statement.loc[key, year]
                variable_names[variable_name] = abs(income_statement.loc[key, year].item())

                # Calculate Pretax Income per Share only for the 'Pretax Income' key
                if key == 'Pretax Income' and outstanding_shares:
                    print(f"Pretax Income for {ticker} {year}: {value}")  # Print Pretax Income
                    pretax_per_share = value / outstanding_shares
                    market_cap_calc = pretax_per_share * outstanding_shares
                    print(f"Market Cap for {ticker}: {market_cap_calc}")
                    print(f"Pretax Income per Share for {ticker} {year}: {pretax_per_share}")
                    Equity_Bond = (pretax_per_share / current_price) * 100
                    print(f"Equity Bond for {ticker} {year}: {Equity_Bond.item()}%")


            except KeyError:
                variable_names[variable_name] = 0  # Return 0 if key doesn't exist

        # loop through the years and each key for the balance sheet
        for key in balance_sheet_keys:
            variable_name = f"{key.replace(' ', '_')}_{year}"  # Unique variable for each year
            try:
                variable_names[variable_name] = abs(balance_sheet.loc[key, year].item())
            except KeyError:
                variable_names[variable_name] = 0  # Return 0 if key doesn't exist

        for key in cashflow_statement_keys:
            variable_name = f"{key.replace(' ', '_')}_{year}"  # Unique variable for each year
            try:
                value = cashflow_statement.loc[key, year]

                # Check if the value exists (it should not be empty or NaN)
                if isinstance(value, pd.Series):
                    if not value.empty:
                        variable_names[variable_name] = abs(value.values[0])  # Use .values[0] to get the scalar
                    else:
                        variable_names[variable_name] = 0  # Default to 0 if the value is empty
                elif pd.notna(value):  # Handle the case where it's not NaN
                    variable_names[variable_name] = abs(value)  # It's already a scalar
                else:
                    variable_names[variable_name] = 0  # Default to 0 if NaN or empty
            except KeyError:
                variable_names[variable_name] = 0  # Return 0 if key doesn't exist

    return variable_names  # Return the dictionary with variable names and values

def generate_sankey(company, selected_year, company_dataframe):
    # Extract the company name from the company (strip "/item/" part)
    if (company and selected_year) or (company and company.startswith('/item/')):
        # Determine the correct company name
        company_name = company.split('/')[-1] if company.startswith('/item/') else company
        print(f"Displaying details for {company_name}")  # Debugging

        # Normalize company name to match entries in your DataFrame
        company_name_normalized = company_name.strip().lower()

        # Assuming you have a 'Normalized_Company' column for matching in your DataFrame
        company_dataframe['Normalized_Company'] = company_dataframe['Company'].str.strip().str.lower()

        # Get the ticker corresponding to the company
        matched_tickers = company_dataframe[company_dataframe['Normalized_Company'] == company_name_normalized][
            'Ticker']
        print(f"Matched tickers: {matched_tickers}")  # Debugging

        if not matched_tickers.empty:
            ticker = matched_tickers.values[0]
            print(f"Selected ticker: {ticker}")  # Debugging
            # Load financial data for the selected company
            financial_metrics = load_data(ticker, years=[selected_year])  # Load data for the specific year
            #print(financial_metrics.keys())
            if financial_metrics:

                # Extract the financial metrics you need
                total_revenue = financial_metrics[f'Total_Revenue_{selected_year}'] / 1e9
                gross_profit_value = financial_metrics[f'Gross_Profit_{selected_year}'] / 1e9
                cost_revenue = financial_metrics[f'Cost_Of_Revenue_{selected_year}'] / 1e9
                operating_income = financial_metrics[f'Operating_Income_{selected_year}'] / 1e9
                operating_expense = financial_metrics[f'Operating_Expense_{selected_year}'] / 1e9
                tax_provision = financial_metrics[f'Tax_Provision_{selected_year}'] / 1e9
                rnd = financial_metrics[f'Research_And_Development_{selected_year}'] / 1e9
                sga = financial_metrics[f'Selling_General_And_Administration_{selected_year}'] / 1e9
                other = financial_metrics[f'Other_Income_Expense_{selected_year}'] / 1e9
                net_income = financial_metrics[f'Net_Income_{selected_year}'] / 1e9
                ga = financial_metrics[f'General_And_Administrative_Expense_{selected_year}'] / 1e9
                other_operating_expenses = financial_metrics[f'Other_Operating_Expenses_{selected_year}'] / 1e9
                ###################################################

                # initialize market cap bar
                bar_fig = go.Figure()

                # Plot the market cap
                categories = ['Market Cap']
                values = [get_market_cap(ticker)]

                bar_fig.add_trace(go.Bar(
                    x=categories,
                    y=values,
                    marker_color='steelblue'
                ))

                bar_fig.update_layout(
                    title='Financial Summary',
                    xaxis_title='Categories',
                    yaxis_title='Amount (in Billions)',
                    barmode='group',
                    paper_bgcolor='#F8F8FF'
                )
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
                         'Other Expenses',
                         'R&D' #new entry
                         ]

                color_for_nodes = ['steelblue', 'green', 'red', 'green', 'red', 'green', 'red', 'red',
                                   'red', 'red', 'red']

                color_for_links = ['lightgreen', 'PaleVioletRed', 'lightgreen', 'PaleVioletRed',
                                   'lightgreen',
                                   'PaleVioletRed', 'PaleVioletRed', 'PaleVioletRed', 'PaleVioletRed', 'PaleVioletRed']

                # Data
                source = [0, 0, 1, 1, 3, 3, 3, 4, 4, 4]
                target = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                value = [gross_profit_value, cost_revenue, operating_income, operating_expense, net_income,
                         tax_provision, other, sga, other_operating_expenses, rnd]



                link = dict(source=source, target=target, value=value, color=color_link)
                node = dict(label=label, pad=35, thickness=20)
                data = go.Sankey(link=link, node=node)

                # Coordinates for nodes
                x = [0.1, 0.35, 0.35, 0.6,
                     0.6, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85]
                y = [0.40, 0.25, 0.70, 0.1,
                     0.45, 0.0, 0.15, 0.30, 0.45, 0.60, 0.75]
                x = [.001 if v == 0 else .999 if v == 1 else v for v in x]
                y = [.001 if v == 0 else .999 if v == 1 else v for v in y]

                # Calculate percentage
                # Avoid division by zero by checking if the denominator is zero or too small
                def safe_divide(numerator, denominator):
                    return (numerator / denominator) * 100 if denominator and abs(denominator) > 1e-9 else 0

                gross_margin_percentage = safe_divide(gross_profit_value, total_revenue)
                sga_margin_percentage = safe_divide(sga, gross_profit_value)
                net_profit_margin = safe_divide(net_income, total_revenue)
                cost_revenue_margin = safe_divide(cost_revenue, total_revenue)
                # total_revenue_margin = safe_divide(total_revenue, get_market_cap(ticker))  # Uncomment if needed
                operating_profit_margin = safe_divide(operating_income, total_revenue)
                operating_expenses_margin = safe_divide(operating_expense, total_revenue)
                tax_provision_margin = safe_divide(tax_provision, total_revenue)
                rnd_margin_percentage = safe_divide(rnd, gross_profit_value)

                # Add custom hover labels for nodes
                custom_hover_data = [
                    f"Total Revenue: {total_revenue:.2f}B",  # Revenue node (no custom data needed)
                    f"Gross Profit: {gross_profit_value:.2f}B<br>Percentage of Revenue: {gross_margin_percentage:.2f}%",
                    f"Cost of Revenue: {cost_revenue:.2f}B<br>Percentage of Revenue: {cost_revenue_margin:.2f}%",
                    # Cost of Revenues
                    f"Operating Profit: {operating_income:.2f}B<br>Percentage of Revenue: {operating_profit_margin:.2f}%",
                    # Operating Profit
                    f"Operating Expenses: {operating_expense:.2f}B<br>Percentage of Revenue: {operating_expenses_margin:.2f}%",
                    # Operating Expenses
                    f"Net Profit: {net_income:.2f}B<br>Percentage of Revenue: {net_profit_margin:.2f}%",  # Net Profit
                    f"Tax: {tax_provision:.2f}B<br>Percentage of Revenue: {tax_provision_margin:.2f}%",  # Tax
                    "",  # Other
                    f"SG&A: {sga:.2f}B<br>Percentage of Gross Profit: {sga_margin_percentage:.2f}%",
                    "",  # Other Expenses
                    f"R&D: {rnd:.2f}B<br>Percentage of Gross Profit: {rnd_margin_percentage:.2f}%"

                ]

                sankey_fig = go.Figure(data=[go.Sankey(
                    textfont=dict(color="black", size=10),
                    node=dict(
                        pad=35,
                        line=dict(color="white", width=1),
                        label=label,
                        x=x,
                        y=y,
                        customdata=custom_hover_data,  # Add custom hover data
                        hovertemplate="%{customdata}<extra></extra>"  # Use custom hover labels
                    ),
                    link=dict(
                        source=source,
                        target=target,
                        value=value
                    )
                )])

                sankey_fig.update_layout(
                    hovermode='x',
                    title="<span style='font-size:36px;color:steelblue;'><b>KO FY23 Income Statement</b></span>",
                    font=dict(size=10, color='white'),
                    paper_bgcolor='#F8F8FF'
                )

                sankey_fig.update_traces(node_color=color_for_nodes,
                                         link_color=color_for_links)

                # Creating a subplot for the bar chart and Sankey diagram
                fig = make_subplots(
                    rows=1, cols=2,
                    column_widths=[0.05, 0.95],
                    specs=[[{"type": "bar"}, {"type": "sankey"}]]
                )

                # Add bar chart data
                for trace in bar_fig.data:
                    fig.add_trace(trace, row=1, col=1)

                # Add Sankey diagram data
                for trace in sankey_fig.data:
                    fig.add_trace(trace, row=1, col=2)

                fig.update_layout(
                    title_text="Market Cap and Income Statement",
                    paper_bgcolor='#F8F8FF'
                )

                fig.update_yaxes(scaleanchor=None, row=1, col=2)

                # Positioning for Sankey graph
                fig.update_traces(
                    selector=dict(type='sankey'),
                    domain=dict(x=[0.00, 1.00], y=[0.01, 0.5])
                )
                fig['layout']['xaxis'].update(domain=[0.0, .06])  # X domain for the bar chart ###
                fig['layout']['yaxis'].update(domain=[0.22, 1])  # Y domain for the bar chart ###
                fig.show()
                #return fig, {'display': 'block'}




generate_sankey("JPMorgan Chase", '2021', nasdaq_df)
#Coca-Cola Company (The)
#JPMorgan Chase
#Apple Inc.
#Boeing
