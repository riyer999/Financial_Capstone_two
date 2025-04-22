import yfinance as yf
import pandas as pd
import os
import numpy as np
import pickle
from dash import Dash, dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from yahooquery import Ticker
from fuzzywuzzy import process


#test1

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY], meta_tags=[
    {"name": "viewport", "content": "width=device-width, initial-scale=1"}
])
server = app.server

cache_file = 'sp500_company.csv'

def generate_sankey(company, selected_year, company_dataframe):
    # Extract the company name from the company (strip "/item/" part)
    if (company and selected_year) or (company and company.startswith('/item/')):
        # Determine the correct company name
        company_name = company.split('/')[-1] if company.startswith('/item/') else company


        # Normalize company name to match entries in your DataFrame
        company_name_normalized = company_name.strip().lower()

        # Assuming you have a 'Normalized_Company' column for matching in your DataFrame
        company_dataframe['Normalized_Company'] = company_dataframe['Company'].str.strip().str.lower()

        # Get the ticker corresponding to the company
        matched_tickers = company_dataframe[company_dataframe['Normalized_Company'] == company_name_normalized][
            'Ticker']

        if not matched_tickers.empty:
            ticker = matched_tickers.values[0]
            # Load financial data for the selected company
            financial_metrics = load_data(ticker, years=[selected_year])  # Load data for the specific year
            if financial_metrics:

                # Extract the financial metrics you need
                if financial_metrics[f'Total_Revenue_{selected_year}'] < 10e6:  # Less than 10 million
                    scale_factor = 1e6  # Scale to millions
                else:
                    scale_factor = 1e9  # Scale to billions

                total_revenue = financial_metrics[f'Total_Revenue_{selected_year}'] / scale_factor

                tax_provision = financial_metrics[f'Tax_Provision_{selected_year}'] / scale_factor
                rnd = financial_metrics[f'Research_And_Development_{selected_year}'] / scale_factor
                sga = financial_metrics[f'Selling_General_And_Administration_{selected_year}'] / scale_factor
                other = financial_metrics[f'Other_Income_Expense_{selected_year}'] / scale_factor
                net_income = financial_metrics[f'Net_Income_{selected_year}'] / scale_factor
                ga = financial_metrics[f'General_And_Administrative_Expense_{selected_year}'] / scale_factor
                other_operating_expenses = financial_metrics[f'Other_Operating_Expenses_{selected_year}'] / scale_factor
                depreciation_amortization_depletion = financial_metrics[f'Depreciation_Amortization_Depletion_Income_Statement_{selected_year}'] / scale_factor

                # values that make up non interest expenses because the API doesn't get that value
                selling_and_marketing_expense = financial_metrics.get(f'Selling_General_And_Administration_{selected_year}', 0) / scale_factor
                occupancy_and_equipment = financial_metrics.get(f'Occupancy_And_Equipment_{selected_year}', 0) / scale_factor
                salaries_and_wages = financial_metrics.get(f'Salaries_And_Wages_{selected_year}', 0) / scale_factor
                professional_expenses = financial_metrics.get(f'Professional_Expense_And_Contract_Services_Expense_{selected_year}', 0) / scale_factor
                other_non_interest = financial_metrics.get(f'Other_Non_Interest_Expense_{selected_year}', 0) / scale_factor
                
                non_interest_expense = (selling_and_marketing_expense + occupancy_and_equipment + salaries_and_wages + professional_expenses + other_non_interest)
                
                # gross profit should be the total revenue - the cost of revenues but cost of revenues is hard to get
                interest_expense = financial_metrics.get(f'Interest_Expense_{selected_year}', 0) / scale_factor
                gross_profit_bank = total_revenue - interest_expense
                gross_profit_value = financial_metrics.get(f'Gross_Profit_{selected_year}', None) / scale_factor
                if gross_profit_value is None or gross_profit_value == 0:
                    gross_profit_value = gross_profit_bank

                
                # interest expense is only one thing that goes into it - its a sort of placeholder
                cost_revenue = financial_metrics.get(f'Cost_Of_Revenue_{selected_year}', None) / scale_factor
                if cost_revenue is None or cost_revenue == 0:
                    cost_revenue = interest_expense

                # operating profit is the sum of the two nodes after it that were already functional
                operating_income = financial_metrics.get(f'Operating_Income_{selected_year}', None) / scale_factor
                operating_income_bank = tax_provision + net_income
                if operating_income is None or operating_income == 0:
                    operating_income = operating_income_bank
                
                
                # most of the issues lie here - hardly any of these are in yfinance api
                operating_expense = financial_metrics.get(f'Operating_Expense_{selected_year}', None) / scale_factor
                if operating_expense is None or operating_expense == 0:
                    operating_expense = non_interest_expense

                

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

                # Define labels
                label = [
                    'Revenue',
                    'Gross Profit',
                    'Cost of Revenues',
                    'Operating Profit',
                    'Operating Expenses',
                    'Net Profit',
                    'Tax',
                    'Other',
                    'SG&A',
                    'Other Expenses',
                    'R&D',
                    'Depreciation Amortization Depletion'
                ]

                # Default colors (Green for profit, Red for expenses/loss)
                color_for_nodes = ['steelblue', 'green', 'red', 'green', 'red', 'green', 'red', 'red', 'red', 'red',
                                   'red', 'red']
                color_for_links = ['lightgreen', 'PaleVioletRed', 'lightgreen', 'PaleVioletRed', 'lightgreen',
                                   'PaleVioletRed', 'PaleVioletRed', 'PaleVioletRed', 'PaleVioletRed', 'PaleVioletRed', 'PaleVioletRed']

                # Data
                source = [0, 0, 1, 1, 3, 3, 3, 4, 4, 4, 4]
                target = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
                value = [
                    gross_profit_value, cost_revenue, operating_income, operating_expense,
                    net_income, tax_provision, other, sga, other_operating_expenses, rnd,
                    depreciation_amortization_depletion
                ]


                # Adjust colors based on negative values
                if gross_profit_value < 0:
                    color_for_nodes[1] = 'red'  # Gross Profit node turns red
                    color_for_links[0] = 'red'  # Link from Revenue to Gross Profit turns red

                if operating_income < 0:
                    color_for_nodes[3] = 'red'  # Operating Profit node turns red
                    color_for_links[2] = 'red'  # Link from Gross Profit to Operating Profit turns red

                if net_income < 0:
                    color_for_nodes[5] = 'red'  # Net Profit node turns red
                    color_for_links[4] = 'red'  # Link from Operating Profit to Net Profit turns red

                #value = [
                    #v if v > 0 else 1e-6  # If v is 0, set it to 1e-6
                    #for v in [
                        #gross_profit_value, cost_revenue, operating_income, operating_expense,
                        #net_income, tax_provision, other, sga, other_operating_expenses, rnd, depreciation_amortization_depletion
                    #]
                #]

                nodes_to_remove = [i for i, v in enumerate(value) if v == 0]

                filtered_source = [s for i, s in enumerate(source) if i not in nodes_to_remove]
                filtered_target = [t for i, t in enumerate(target) if i not in nodes_to_remove]
                filtered_value = [v for i, v in enumerate(value) if i not in nodes_to_remove]

                link = dict(source=filtered_source, target=filtered_target, value=filtered_value, color=color_link)
                node = dict(label=label, pad=35, thickness=20)
                data = go.Sankey(link=link, node=node)

                # Coordinates for nodes
                x = [0.1, 0.35, 0.35, 0.6,
                     0.6, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85]
                y = [0.40, 0.25, 0.70, 0.1,
                     0.45, 0.0, 0.15, 0.30, 0.45, 0.60, 0.75, 0.90]
                x = [.001 if v == 0 else .999 if v == 1 else v for v in x]
                y = [.001 if v == 0 else .999 if v == 1 else v for v in y]

                # Calculate percentage
                # Avoid division by zero by checking if the denominator is zero or too small
                def safe_divide(numerator, denominator):
                    return (numerator / denominator) * 100 if denominator and abs(denominator) > 1e-9 else 0

                gross_margin_percentage = safe_divide(gross_profit_value, total_revenue)
                other_percentage = safe_divide(other, total_revenue)
                sga_margin_percentage = safe_divide(sga, gross_profit_value)
                net_profit_margin = safe_divide(net_income, total_revenue)
                cost_revenue_margin = safe_divide(cost_revenue, total_revenue)
                # total_revenue_margin = safe_divide(total_revenue, get_market_cap(ticker))  # Uncomment if needed
                operating_profit_margin = safe_divide(operating_income, total_revenue)
                operating_expenses_margin = safe_divide(operating_expense, total_revenue)
                tax_provision_margin = safe_divide(tax_provision, total_revenue)
                rnd_margin_percentage = safe_divide(rnd, gross_profit_value)
                depreciation_amortization_depletion_margin_percentage = safe_divide(depreciation_amortization_depletion, gross_profit_value)
                other_operating_expenses_percentage = safe_divide(other_operating_expenses, gross_profit_value)

                # Add custom hover labels for nodes
                unit = "M" if scale_factor == 1e6 else "B"


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
                    f"Other Expenses: {other:.2f}B<br>Percentage of Revenue: {other_percentage:.2f}%",
                    f"SG&A: {sga:.2f}B<br>Percentage of Gross Profit: {sga_margin_percentage:.2f}%",
                    f"Other Expenses: {other_operating_expenses:.2f}{unit}<br>Percentage of Gross Profit: {other_operating_expenses_percentage:.2f}%",  # Other Expenses
                    f"R&D: {rnd:.2f}B<br>Percentage of Gross Profit: {rnd_margin_percentage:.2f}%",
                    f"Depreciation Amortization Depletion: {depreciation_amortization_depletion:.2f}B<br>Percentage of Gross Profit: {depreciation_amortization_depletion_margin_percentage:.2f}%"

                ]

                sankey_fig = go.Figure(data=[go.Sankey(
                    textfont=dict(color="white", size=10), #black
                    node=dict(
                        pad= 12, #from 35
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
                    title=f"<span style='font-size:36px;color:white;'><b>Income Statement</b></span>",
                    font=dict(size=10, color='white'),
                    paper_bgcolor='#121212',  # Black background
                    plot_bgcolor='#121212',   # Black plot background
    )

                sankey_fig.update_traces(node_color=color_for_nodes,
                                         link_color=color_for_links)

                # Creating a subplot for the bar chart and Sankey diagram
                fig = make_subplots(
                    rows=1, cols=1,  # Only one column
                    specs=[[{"type": "sankey"}]]  # Only Sankey diagram
                )

                # Add Sankey diagram data
                for trace in sankey_fig.data:
                    fig.add_trace(trace, row=1, col=1)

                fig.update_layout(
                    title_text=f"Income Statement Visual for {ticker} ({selected_year})",
                    paper_bgcolor='#0c0c0d',
                    font=dict(color='white')
                )


                # Positioning for Sankey graph
                fig.update_traces(
                    selector=dict(type='sankey'),
                    domain=dict(x=[0.00, 0], y=[0.01, 0])
                )

                return fig, {'display': 'block'}

def generate_balance_visual(company, selected_year, company_dataframe):
    if (company and selected_year) or (company and company.startswith('/item/')):
        # Determine the correct company name
        company_name = company.split('/')[-1] if company.startswith('/item/') else company

        # Normalize company name to match entries in your DataFrame
        company_name_normalized = company_name.strip().lower()

        # Assuming you have a 'Normalized_Company' column for matching in your DataFrame
        company_dataframe['Normalized_Company'] = company_dataframe['Company'].str.strip().str.lower()

        # Get the ticker corresponding to the company
        matched_tickers = company_dataframe[company_dataframe['Normalized_Company'] == company_name_normalized][
            'Ticker']

    if not matched_tickers.empty:
        ticker = matched_tickers.values[0]
        financial_metrics = load_data(ticker, years=[selected_year])  # Load data for the specific year
        print(f"this is financial metrics {financial_metrics}")

        # Replace this with actual financial metrics from `financial_data`
        data = {
            "root": [],
            "category": [],
            "subcategory": [],
            "type": [],
            "item": [],
            "value": []
        }

        # Define hierarchy for treemap with a root node


        hierarchy = {

            "Total Assets": {
                "Current Assets": {
                    "Cash Cash Equivalents And Short Term Investments": [
                        "Cash Cash Equivalents And Short Term Investments",
                        "Cash And Cash Equivalents",
                        'Cash Financial',
                        "Restricted Cash"
                    ],
                    "Receivables": [
                        "Receivables",
                    ],
                    "Inventory": [
                        "Raw Materials",
                        "Finished Goods",
                        "Work In Process",
                        "Other Inventories",
                    ],
                    "Prepaid Assets": [
                        "Prepaid Assets",
                    ],
                    "Other": [
                        "Other Current Assets",
                    ],
                    "Cash and Other":[
                        "Cash Cash Equivalents And Federal Funds Sold"
                    ],
                    "Short Term Investments":[
                        "Other Short Term Investments",
                    ]
                },
                "Total Non-current Assets": {
                    "Net PPE": [
                        "Net PPE",
                    ],
                    "Goodwill": [
                        "Goodwill And Other Intangible Assets",
                    ],
                    "Investments And Advances": [
                        "Investments And Advances",

                    ],
                    "Additional Assets": [
                        "Financial Assets",
                    ],
                    "Non Current Accounts Receivable": [
                        "Non Current Accounts Receivable",
                    ],
                    "Long Term Equity Investment ":[
                        "Long Term Equity Investment",
                    ],
                    "Non Current Receivables": [
                        "Non Current Note Receivables",
                    ],
                    "Non Current Deferred Assets": [
                        "Non Current Deferred Assets",
                    ],
                    "Defined Benefit": [
                        "Defined Pension Benefit",
                    ],
                    "Other": [
                        "Other Non Current Assets",
                    ]
                }
            },
            "Total Liabilities and Equity": {
                "Total Liabilities": {
                    "Current Liabilities": [
                        "Payables And Accrued Expenses",
                        "Pensionand Other Post Retirement Benefit Plans Current",
                        "Current Debt And Capital Lease Obligation",
                        "Other Current Liabilities",
                        "Current Provisions",
                        "Current Deferred Liabilities",
                        'Derivative Product Liabilities'
                        'Other Current Borrowings',
                    ],
                    "Total Non Current Liabilities Net Minority Interest": [
                        "Long Term Debt And Capital Lease Obligation",
                        "Non Current Deferred Liabilities",
                        "Other Non Current Liabilities",
                        "Tradeand Other Payables Non Current",
                        "Long Term Provisions"
                        #"Preferred Securities Outside Stock Equity"
                    ],
                    "Total Deposits":[
                        "Deposits"
                    ],
                    "Other Liabilities": [
                        "Other Liabilities"
                    ],
                    "Policy Holders liabilities":[
                        "LiabilityForClaimsAndClaimsAdjustmentExpensePropertyCasualtyLiability",
                        "LiabilityForFuturePolicyBenefits",
                        "PolicyholderContractDeposits",
                        "UnearnedPremiums",
                        "ClaimPaymentsOutstanding",
                        "AccruedLiabilitiesAndOtherLiabilities"
                    ]

                },
                "Total Equity": {
                    "Equity": [
                        "Stockholders Equity"
                    ],
                    "Interest": [
                        "Minority Interest"
                    ]
                }
            }
        }

        # Dynamically build data for the treemap
        for category, subcategories in hierarchy.items():
            for subcategory, types in subcategories.items():
                for type_, items in types.items():
                    for item in items:
                        # Retrieve the corresponding financial metric for the selected year
                        metric_key = f"{item.replace(' ', '_')}_{selected_year}"
                        value = financial_metrics.get(metric_key, 0) / 1e9  # Convert to billions for visualization

                        # Append data for treemap
                        data["root"].append(f"Balance Sheet Visual for {ticker} ({selected_year})")  # Add root node
                        data["category"].append(category)
                        data["subcategory"].append(subcategory)
                        data["type"].append(type_)
                        data["item"].append(item)
                        data["value"].append(value)

        # Create the treemap
        if not isinstance(data, pd.DataFrame):
            data = pd.DataFrame(data)

        # Add a custom hover label that appends "Billion" to the value
        data['custom_label'] = data['item'] + ': $' + data['value'].astype(str) + ' Billion'

        # Create the treemap
        balance_fig = px.treemap(
            data,
            path=['root', 'category', 'subcategory', 'type', 'item'],  # Include root node in path
            values='value'
        )

        # Update hover labels using hovertemplate
        balance_fig.update_traces(
            maxdepth=4,  # Adjust depth to include all levels
            hovertemplate='<b>%{label}</b><br>%{value} Billion<extra></extra>',
            textfont=dict(size=23)  # Adjust the font size
        )

        # Update layout
        balance_fig.update_layout(
        margin=dict(t=50, l=50, r=50, b=50),
        paper_bgcolor='#121212',  # Black background
        plot_bgcolor='#121212',   # Black plot background
        font=dict(color='white')  # White font
        )

        # Show the plot
        #balance_fig.show()
        return balance_fig


def generate_cashflow_visual(company, selected_year, company_dataframe):
    if (company and selected_year) or (company and company.startswith('/item/')):
        # Determine the correct company name
        company_name = company.split('/')[-1] if company.startswith('/item/') else company

        # Normalize company name to match entries in DataFrame
        company_name_normalized = company_name.strip().lower()
        company_dataframe['Normalized_Company'] = company_dataframe['Company'].str.strip().str.lower()

        # Get the ticker corresponding to the company
        matched_tickers = company_dataframe[company_dataframe['Normalized_Company'] == company_name_normalized][
            'Ticker']

    if not matched_tickers.empty:
        ticker = matched_tickers.values[0]

        # Load only relevant cash flow statement data
        financial_metrics_all_years = load_data(ticker,
                                                years=['2021', '2022', '2023', '2024'])  # Load data for all years

        # Extract only the cash flow statement-related keys
        cash_flow_keys = [
            'Operating_Cash_Flow', 'Issuance_Of_Debt', 'Capital_Expenditure',
            'Repayment_Of_Debt', 'Repurchase_Of_Capital_Stock', 'Cash_Dividends_Paid',
            'Sale_Of_Investment', 'Issuance_Of_Capital_Stock', 'Purchase_Of_Investment'
        ]

        # Initialize max_value for scaling the y-axis
        max_value = 0

        # Loop through the relevant keys and years to calculate the maximum value
        for year in ['2021', '2022', '2023', '2024']:
            for key in cash_flow_keys:
                # Build the key for the specific year (e.g., 'Operating_Cash_Flow_2024')
                year_key = f'{key}_{year}'

                # Check if the key exists and update max_value
                if year_key in financial_metrics_all_years:
                    max_value = max(max_value, financial_metrics_all_years[year_key])

        # Prepare data for the selected year
        op_cash_flow = financial_metrics_all_years.get(f'Operating_Cash_Flow_{selected_year}', 0)
        issuance_debt = financial_metrics_all_years.get(f'Issuance_Of_Debt_{selected_year}', 0)

        capital_expenditure = abs(financial_metrics_all_years.get(f'Capital_Expenditure_{selected_year}', 0))
        repayment_debt = abs(financial_metrics_all_years.get(f'Repayment_Of_Debt_{selected_year}', 0))
        repurchase_stock = abs(financial_metrics_all_years.get(f'Repurchase_Of_Capital_Stock_{selected_year}', 0))
        dividends_paid = abs(financial_metrics_all_years.get(f'Cash_Dividends_Paid_{selected_year}', 0))

        sale_of_investment = abs(financial_metrics_all_years.get(f'Sale_Of_Investment_{selected_year}', 0))
        issuance_of_capital_stock = abs(
            financial_metrics_all_years.get(f'Issuance_Of_Capital_Stock_{selected_year}', 0))
        purchase_of_investment = abs(financial_metrics_all_years.get(f'Purchase_Of_Investment_{selected_year}', 0))

        # Create lists for inflows and outflows
        money_in_categories = []
        money_in_values = []
        money_out_categories = []
        money_out_values = []

        # Operating cash flow: inflow or outflow based on value
        if op_cash_flow >= 0:
            money_in_categories.append('Operating Cash Flow')
            money_in_values.append(op_cash_flow)
        else:
            money_out_categories.append('Operating Cash Flow')
            money_out_values.append(abs(op_cash_flow))  # Make it positive for plotting

        # Issuance of debt as inflow
        money_in_categories.append('Issuance Of Debt')
        money_in_values.append(issuance_debt)

        # New inflows
        if sale_of_investment > 0:
            money_in_categories.append('Sale Of Investment')
            money_in_values.append(sale_of_investment)

        if issuance_of_capital_stock > 0:
            money_in_categories.append('Issuance Of Capital Stock')
            money_in_values.append(issuance_of_capital_stock)

        # Outflows
        money_out_categories.extend([
            'Capital Expenditure', 'Repayment Of Debt', 'Repurchase Of Capital Stock', 'Cash Dividends Paid',
            'Purchase Of Investment'
        ])
        money_out_values.extend([
            capital_expenditure, repayment_debt, repurchase_stock, dividends_paid, purchase_of_investment
        ])

        year_data = {
            'Year': selected_year,
            'Category1': money_in_categories,
            'Value1': money_in_values,
            'Category2': money_out_categories,
            'Value2': money_out_values
        }

        # Create subplots
        cash_fig = make_subplots(rows=1, cols=2, subplot_titles=("Money In", "Money Out"))

        # Add traces for money in and money out
        cash_fig.add_trace(go.Bar(
            x=year_data['Category1'],
            y=year_data['Value1'],
            name=f'Year {year_data["Year"]} - Money In',
            marker=dict(color='steelblue')
        ), row=1, col=1)

        cash_fig.add_trace(go.Bar(
            x=year_data['Category2'],
            y=year_data['Value2'],
            name=f'Year {year_data["Year"]} - Money Out',
            marker=dict(color='red')
        ), row=1, col=2)

        # Update layout to set static y-axis range
        cash_fig.update_layout(
            title_text=f"Cash Flow Visual for {ticker} ({selected_year})",
            xaxis_title="",
            yaxis_title="Money in Billions of Dollars",
            showlegend=False,
            font=dict(color='white', size=14),
            paper_bgcolor='#121212',  # Black background
            plot_bgcolor='#121212',  # Black plot background

            xaxis=dict(
                tickmode='array',
                tickvals=['Operating Cash Flow', 'Issuance Of Debt', 'Capital Expenditure', 'Repayment Of Debt',
                          'Repurchase Of Capital Stock', 'Sale Of Investment', 'Issuance Of Capital Stock',
                          'Purchase Of Investment'],
                ticktext=['Operating Cash Flow', 'Issuance Of Debt', 'Capital Expenditure', 'Repayment Of Debt',
                          'Repurchase Of Capital Stock', 'Sale Of Investment', 'Issuance Of Capital Stock',
                          'Purchase Of Investment']
            ),
            yaxis=dict(range=[0, max_value * 1.1]),  # Static y-axis range across all years
            yaxis2=dict(range=[0, max_value * 1.1])  # Same for the second y-axis
        )

        return cash_fig


def generate_equity_bond(company, selected_year, company_dataframe):
    """Generates the equity bond yield visualization for a given company and year."""

    if not company or not selected_year:
        print("DEBUG: Missing company or year")
        return go.Figure()  # Return an empty figure if inputs are invalid

    # Extract and normalize company name
    company_name = company.split('/')[-1] if company.startswith('/item/') else company
    company_name_normalized = company_name.strip().lower()

    # Match the ticker symbol
    company_dataframe['Normalized_Company'] = company_dataframe['Company'].str.strip().str.lower()
    matched_tickers = company_dataframe[company_dataframe['Normalized_Company'] == company_name_normalized]['Ticker']

    if matched_tickers.empty:
        print(f"DEBUG: No ticker found for {company_name}")
        return go.Figure()

    ticker = matched_tickers.values[0]
    
    # Load financial data for the selected year
    financial_metrics = load_data(ticker, years=[selected_year])
    stock = yf.Ticker(ticker)
    stock_info = stock.info

    # Retrieve necessary financial values
    pretax_income = financial_metrics.get(f'Pretax_Income_{selected_year}', 0)
    shares_outstanding = stock_info.get('sharesOutstanding', None)
    stock_price = stock_info.get('currentPrice', None)

    # Debugging missing values
    #if pretax_income == 0:
    #    print(f"DEBUG: Pretax income is missing for {ticker} in {selected_year}")
    #if not shares_outstanding:
    #    print(f"DEBUG: Shares outstanding is missing for {ticker}")
    #if not stock_price:
    #    print(f"DEBUG: Stock price is missing for {ticker}")

    # Ensure valid values before calculation
    if pretax_income == 0 or not shares_outstanding or not stock_price:
        print(f"DEBUG: Missing data for {ticker} in {selected_year}")
        return go.Figure()

    # Calculate Pretax Income Per Share
    pretax_per_share = pretax_income / shares_outstanding
    equity_bond_yield = (pretax_per_share / stock_price) * 100  # Convert to percentage

    print(f"DEBUG: {ticker} {selected_year} - Equity Bond Yield: {equity_bond_yield:.2f}%")

    # Determine graph color
    bar_color = 'red' if equity_bond_yield < 0 else 'green'

    # Determine y-axis range
    y_min = min(equity_bond_yield * 1.2, -5) if equity_bond_yield < 0 else 0
    y_max = max(equity_bond_yield * 1.2, 5)

    # Create bar chart
    fig = go.Figure(go.Bar(
        x=[selected_year],
        y=[equity_bond_yield],
        text=[f"{equity_bond_yield:.2f}%"],
        textposition='outside',
        marker_color= bar_color
    ))

    fig.update_layout(
        title=f"Equity Bond Yield Visual for {ticker} ({selected_year})",
        xaxis_title="Year",
        yaxis_title="Equity Bond Yield (%)",
        #yaxis=dict(range=[0, max(equity_bond_yield * 1.2, 5)]),  # Ensure readable scale
        yaxis=dict(range=[y_min, y_max]),  # Allow negative values
        template="plotly_dark"
    )

    return fig  # Returns only the figure (Dash-friendly)

# Function to safely convert values to float
def safe_float(value):
    try:
        return float(value) if value else 0.0
    except ValueError:
        return 0.0  # Return 0.0 if value can't be converted to float

# Main function to process the data
def load_data(ticker, years=["2021", "2022", "2023", "2024"]):
    ystock = yf.Ticker(ticker)
    ## define the path
    directory_path = "pkl_files"  # Replace with your directory path

    # Combine the directory path and filename to get the full path
    filename = os.path.join(directory_path, f"{ticker}_financials.pkl")

    # Dictionary to store the extracted values
    variable_names = {}

    try:
        # Open and load the pickle file
        with open(filename, "rb") as f:
            data = pickle.load(f)  # Load the dictionary from the file

        # Extract the required years from the loaded data
        for concept in data:
            # Check if the concept contains a year, then add it to the dictionary
            for year in years:
                if f"_{year}" in concept:
                    variable_names[concept] = data[concept]

    except FileNotFoundError:
        print(f"Warning: {filename} not found. Skipping...")
    except Exception as e:
        print(f"Error loading {filename}: {e}")


    #print(variable_names)
    # Fetch the financial data
    income_statement = ystock.incomestmt

    balance_sheet = ystock.balance_sheet
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    #print(balance_sheet)
    cashflow_statement = ystock.cashflow  # This fetches the cash flow statement
    print(cashflow_statement)
    # Fetch the stock's information (including shares outstanding)
    stock_info = ystock.info
    outstanding_shares = stock_info.get('sharesOutstanding')
    current_price = stock_info.get('currentPrice')

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
        'General And Administrative Expense',
        'Research And Development',
        'Gross Profit',
        'Cost Of Revenue',
        'Total Revenue',
        'Operating Revenue',
        'Pretax Income',
        'Depreciation Amortization Depletion Income Statement',
        'Total Expenses'
    ]

    balance_sheet_keys = [
        'Total Assets',
        'Cash Cash Equivalents And Federal Funds Sold',
        'Current Assets',
        'Cash Cash Equivalents And Short Term Investments',
        'Cash And Cash Equivalents',
        'Cash',
        'Cash Financial',
        'Cash Equivalents',
        'Other Short Term Investments',
        'Receivables',
        'Inventory',
        'Raw Materials',
        'Finished Goods',
        'Work In Process',
        'Other Inventories',
        'Prepaid Assets',
        'Restricted Cash',
        'Other Current Assets',
        #
        'Total Non Current Assets',
        'Long Term Equity Investment',
        'Net PPE',
        'Investments And Advances',
        'Financial Assets',
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
        'Other Current Borrowings',
        'Current Liabilities',
        'Payables And Accrued Expenses',
        'Pensionand Other Post Retirement Benefit Plans Current',
        'Current Provisions',
        'Current Deferred Liabilities',
        'Current Debt And Capital Lease Obligation',
        'Other Current Liabilities',
        'Total Non Current Liabilities Net Minority Interest',
        'Long Term Provisions',
        'Preferred Securities Outside Stock Equity',
        'Long Term Debt And Capital Lease Obligation',
        'Non Current Deferred Liabilities',
        'Other Non Current Liabilities',
        'Derivative Product Liabilities',
        'Tradeand Other Payables Non Current',
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
        'Sale Of Investment', # new
        'Issuance of Capital Stock', # new

        'Capital Expenditure',
        'Repayment Of Debt',
        'Repurchase Of Capital Stock',
        'Cash Dividends Paid',
        'Purchase Of Investment' # new


    }

    # loop through the years and each key for the income statement
    for year in years:
        for key in income_statement_keys:
            variable_name = f"{key.replace(' ', '_')}_{year}"  # Unique variable for each year
            try:
                value = income_statement.loc[key, year]

                # Check if it's a valid scalar value or Series
                if isinstance(value, (np.ndarray, pd.Series)) and value.size == 1:
                    # If it's a single value, safely get it using .item()
                    variable_names[variable_name] = value.item() if pd.notna(value.item()) else 0
                else:
                    # If it's a Series or other non-scalar, handle it safely
                    if pd.notna(value).all():  # Check if all values are non-NaN
                        variable_names[variable_name] = value
                    else:
                        variable_names[variable_name] = 0  # Set to 0 if there's any missing data

                # Calculate Pretax Income per Share only for the 'Pretax Income' key
                if key == 'Pretax Income' and outstanding_shares:
                    pretax_per_share = value / outstanding_shares
                    market_cap_calc = pretax_per_share * outstanding_shares
                    Equity_Bond = (pretax_per_share / current_price) * 100
                    #if isinstance(Equity_Bond, (np.ndarray, pd.Series)):
                        #if Equity_Bond.size == 1:
                            #print(f"Equity Bond for {ticker} {year}: {Equity_Bond.item()}%")
                        #else:
                            #print(f"Equity Bond for {ticker} {year}: Multiple values or missing data")
                    #else:
                        #print(f"Equity Bond for {ticker} {year}: {Equity_Bond}%")



            except KeyError:
                variable_names[variable_name] = 0  # Return 0 if key doesn't exist

        # loop through the years and each key for the balance sheet
        cash_and_cash_equivalents = None
        cash_and_short_term_investments = None
        other_short_term_investments = None
        total_liabilities_calculated = 0
        total_liabilities_reported = None

        # List of keys representing liabilities
        liabilities_keys = [
            "Payables And Accrued Expenses",
            "Pensionand Other Post Retirement Benefit Plans Current",
            "Current Debt And Capital Lease Obligation",
            "Other Current Liabilities",
            "Current Provisions",
            "Current Deferred Liabilities",
            'Derivative Product Liabilities',
            'Other Current Borrowings',
            "Long Term Debt And Capital Lease Obligation",
            "Non Current Deferred Liabilities",
            "Other Non Current Liabilities",
            "Tradeand Other Payables Non Current",
            "Long Term Provisions"
        ]

        for key in balance_sheet_keys:
            variable_name = f"{key.replace(' ', '_')}_{year}"  # Unique variable for each year
            try:
                value = balance_sheet.loc[key, year]


                # Print the value for each key to debug
                #print(f"Processing {key} for {year}: {value}")

                # Store the value if it exists
                if not value.empty:
                    variable_names[variable_name] = abs(value.iloc[0])
                else:
                    variable_names[variable_name] = 0

                # Capture values for conditional logic
                if key == 'Cash And Cash Equivalents':
                    cash_and_cash_equivalents = abs(value.iloc[0]) if pd.notna(value.iloc[0]) else 0
                    #print(f"Cash And Cash Equivalents for {year}: {cash_and_cash_equivalents}")

                if key == 'Cash Cash Equivalents And Short Term Investments':
                    cash_and_short_term_investments = abs(value.iloc[0]) if pd.notna(value.iloc[0]) else 0
                    #print(
                        #f"Cash Cash Equivalents And Short Term Investments for {year}: {cash_and_short_term_investments}")

                if key == 'Other Short Term Investments':
                    other_short_term_investments = abs(value.iloc[0]) if pd.notna(value.iloc[0]) else 0
                    #print(f"Other Short Term Investments for {year}: {other_short_term_investments}")

            except KeyError:
                variable_names[variable_name] = 0
                #print(f"KeyError for {key} in {year}, setting to 0")


        # Final conditional logic outside the loop
        # Handle "Cash And Cash Equivalents"
        if cash_and_short_term_investments and cash_and_short_term_investments > 0:
            variable_names[f"Cash_And_Cash_Equivalents_{year}"] = 0
        else:
            variable_names[
                f"Cash_And_Cash_Equivalents_{year}"] = cash_and_cash_equivalents if cash_and_cash_equivalents is not None else 0

        # Handle "Other Short Term Investments"
        if cash_and_short_term_investments and cash_and_short_term_investments > 0:
            variable_names[f"Other_Short_Term_Investments_{year}"] = 0
        else:
            variable_names[
                f"Other_Short_Term_Investments_{year}"] = other_short_term_investments if other_short_term_investments is not None else 0



        for key in cashflow_statement_keys:
            variable_name = f"{key.replace(' ', '_')}_{year}"  # Unique variable for each year
            try:
                value = cashflow_statement.loc[key, year]

                # Check if the value exists (it should not be empty or NaN)
                if isinstance(value, pd.Series):
                    if not value.empty:
                        variable_names[variable_name] = (value.values[0])  # Use .values[0] to get the scalar
                    else:
                        variable_names[variable_name] = 0  # Default to 0 if the value is empty
                elif pd.notna(value):  # Handle the case where it's not NaN
                    variable_names[variable_name] = (value)  # It's already a scalar
                else:
                    variable_names[variable_name] = 0  # Default to 0 if NaN or empty
            except KeyError:
                variable_names[variable_name] = 0  # Return 0 if key doesn't exist
    #print(variable_names)
    return variable_names  # Return the dictionary with variable names and values


# Function to get market capitalization from Yahoo Finance
def get_market_cap(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    market_cap = stock.info.get('marketCap', None)
    return market_cap


# Check if cache file exists
if os.path.exists(cache_file):
    # Load cached data if it exists
    cached_data = pd.read_csv(cache_file)
    #print("Loaded market cap data from cache.")
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

# Calculate total market cap per industry
industry_market_caps = cached_data.groupby('Industry')['MarketCap'].sum().reset_index()
industry_market_caps.columns = ['Industry', 'TotalMarketCap']

# Merge total market cap back into the main DataFrame
treemap_df = pd.merge(cached_data, industry_market_caps, on='Industry')


# Create the treemap plot using Plotly Express with darker colors
def create_treemap():
    fig = px.treemap(
        treemap_df,
        path=[px.Constant("S&P 500"), 'Industry', 'Company'],
        values='MarketCap',
        color='MarketCap',
        color_continuous_scale=[(0.0, '#1B2A49'), (0.5, '#1E6091'), (1.0, '#76C1EC')]

    )

    fig.update_traces(
        hovertemplate=(
                '<b>Company:</b> %{label}<br>' +
                '<b>Market Cap:</b> $%{value:,.2f}<extra></extra>'
        )
    )
    fig.update_layout(
        plot_bgcolor='#010103',
        paper_bgcolor='#010103',
        font_color='#e6e6e6',
        width=1310,
        height=850,
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0)
    )
    return fig


# Assuming treemap_df and nasdaq_df exist with relevant data
def get_company_ticker(company_name, treemap_df, nasdaq_df):
    # Normalize input company name
    company_name_normalized = company_name.strip().lower()

    # Function to find the best match in a DataFrame
    def search_dataframe(df):
        company_names = df['Company'].str.strip().str.lower().tolist()
        best_match, score = process.extractOne(company_name_normalized, company_names)
        if score > 85:  # Adjust threshold as needed
            matched_ticker = df.loc[df['Company'].str.strip().str.lower() == best_match, 'Ticker']
            return matched_ticker.values[0] if not matched_ticker.empty else None
        return None

    # Search in treemap_df first, then fallback to nasdaq_df
    ticker = search_dataframe(treemap_df) or search_dataframe(nasdaq_df)
    return ticker

def get_company_summary(company_name, treemap_df, nasdaq_df):
    # Get the ticker dynamically
    ticker = get_company_ticker(company_name, treemap_df, nasdaq_df)
    if not ticker:
        return f"Company '{company_name}' not found."

    # Fetch company summary
    stock = Ticker(ticker)
    summary = stock.asset_profile.get(ticker, {}).get('longBusinessSummary', 'Summary not available.')
    return summary


def simple_summarizer(text):
    # Placeholder for future summarization
    return text

# Step 1: Read the file into a DataFrame
file_path = 'sp500_company.csv'  # Replace with the path to your file
nasdaq_df = pd.read_csv(file_path)
nasdaq_df = pd.read_csv(file_path, dtype={'MarketCap': float}, low_memory=False)

# Step 2: Process the data to create autocomplete options
autocomplete_options = [
    {"label": f"{company_name} ({ticker})", "value": ticker}
    for company_name, ticker in zip(nasdaq_df['Company'], nasdaq_df['Ticker'])
]

autocomplete_options1 = [
    {"label": f"{company_name}", "value": company_name} for company_name, ticker in
    zip(treemap_df['Company'].values, treemap_df['Ticker'].values)
]

# App layout
app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),

    # Sidebar
    html.Div(id='sidebar', children=[
        html.Div([
            html.H1([
                "FinSight",
                html.Br(),
                html.Span("Visualization of Company Financials")
            ], style={'color': '#e6e6e6'}),
            html.P("Search or Click on a Company to view their financials!", style={'color': '#cccccc', 'font-size': '18px'})
        ], style={"vertical-align": "top", "height": 320}),  

        # Buttons Section with Fixed Spacing
        html.Div([
            dbc.RadioItems(
                className='btn-group',
                inputClassName='btn-check',
                labelClassName="btn btn-outline-light",
                labelCheckedClassName="btn btn-light",
                options=[
                    {"label": "Home", "value": 1},
                    {"label": "Compare", "value": 2}
                ],
                value=1,
                id='compare-button',
                style={'display': 'flex', 'gap': '15px'}  # Adds spacing between buttons
            ),
        ], style={'margin-bottom': '15px'}),  # Adds spacing below buttons

        # Search Bar Section
        html.Div([
            dcc.Dropdown(
                id="autocomplete-dropdown",
                options=autocomplete_options,
                placeholder="Search Company...",
                style={'width': '100%', 'backgroundColor': '#FFFFFC', 'color': '#000000'},
                searchable=True,
                multi=False,
            ),
        ], style={'margin-top': '10px', 'width': '100%'}),  # Positioned below buttons

    ], style={'width': 300, 'margin-left': 25, 'margin-top': 35}),  # Sidebar adjustments

    # Main Content Area
    html.Div(id='page-content', style={'width': 890, 'margin': 40})

], fluid=True, style={'display': 'flex', 'backgroundColor': '#010103'}) 

# Define page layouts
main_page_layout = html.Div([
    dcc.Graph(id='treemap-graph', figure=create_treemap())
])
@app.callback(
    Output('autocomplete-dropdown1', 'value'),  # Set the dropdown's value
    Input('autocomplete-dropdown1', 'value')  # Triggered when the user types or selects
)
def persist_value(selected_value):
    return selected_value  # Return the same value to keep it displayed
@app.callback(
    [Output("graph1", "figure"), Output("graph1-container", "style"),
     ],
    [Input("autocomplete-dropdown1", "value"), Input("year-dropdown-1", "value")]
)
def update_graph1(company_name, selected_year):
    return generate_sankey(company_name, selected_year, treemap_df)
@app.callback(
    Output("balance-graph-1", "figure"),
    [Input("autocomplete-dropdown1", "value"), Input("year-dropdown-1", "value")]
)
def graph3(company_name, selected_year):
    return generate_balance_visual(company_name, selected_year, treemap_df)
@app.callback(
    [Output("graph2", "figure"), Output("graph2-container", "style")],
    [Input("autocomplete-dropdown2", "value"), Input("year-dropdown-2", "value")]
)
def update_graph2(company_name, selected_year):
    return generate_sankey(company_name, selected_year, treemap_df)
@app.callback(
    Output("balance-graph-2", "figure"),
    [Input("autocomplete-dropdown2", "value"), Input("year-dropdown-2", "value")]
)
def graph4(company_name, selected_year):
    return generate_balance_visual(company_name, selected_year, treemap_df)
def generate_graph(company_name, selected_year):
    return generate_sankey(company_name, selected_year, treemap_df) #new concise way of calling the sankey code

compare_page_layout = html.Div([
    html.H1("Compare Companies"),
    #html.P("Here you can compare different companies."),

    # Wrapper for the two columns
    html.Div([

        html.Div([
            html.Div([
                html.Label("Company 1 Search", style={'color': 'white'}),
                dcc.Dropdown(
                    id="autocomplete-dropdown1",
                    options=autocomplete_options1,
                    placeholder="Company 1 Search...",
                    style={'width': 200, 'backgroundColor': 'white', 'color': 'black'},
                    searchable=True,
                    multi=False,
                ),

            ], style={'padding': '10px'}),

            html.Div([
                html.Label("Select Year", style={'color': 'white'}),
                dcc.Dropdown(
                    id="year-dropdown-1",
                    options=[{"label": str(year), "value": str(year)} for year in range(2021, 2025)],
                    placeholder="Select Year"
                ),
            ], style={'padding': '10px'}),

            # Graph 1
            html.Div([
                dcc.Graph(id="graph1", style={'width': '100%', 'height': '70vh'}),  # Increased graph height
            ], id="graph1-container", style={'padding': '10px', 'display': 'block'}),

            # New Graph: balance-graph-1
            dcc.Graph(id="balance-graph-1", style={'width': '100%', 'height': '70vh'}),  # New graph 1

        ], style={'flex': '2', 'padding': '10px', 'border': '1px solid #ccc'}),

        html.Div([
            html.Div([
                html.Label("Company 2 Search", style={'color': 'white'}),
                dcc.Dropdown(
                    id="autocomplete-dropdown2",
                    options=autocomplete_options1,
                    placeholder="Company 2 Search...",
                    style={'width': 200, 'backgroundColor': 'white', 'color': 'black'},
                    searchable=True,
                    multi=False,
                ),
            ], style={'padding': '10px'}),

            html.Div([
                html.Label("Select Year", style={'color': 'white'}),
                dcc.Dropdown(
                    id="year-dropdown-2",
                    options=[{"label": str(year), "value": str(year)} for year in range(2021, 2025)],
                    placeholder="Select Year"
                ),
            ], style={'padding': '10px'}),

            # Graph 2
            html.Div([
                dcc.Graph(id="graph2", style={'width': '100%', 'height': '70vh'}),  # Increased graph height
            ], id="graph2-container", style={'padding': '10px', 'display': 'block'}),

            # New Graph: balance-graph-2
            dcc.Graph(id="balance-graph-2", style={'width': '100%', 'height': '70vh'}),  # New graph 2

        ], style={'flex': '2', 'padding': '10px', 'border': '1px solid #ccc'}),
        html.A(
            html.Button("Back to Treemap", id="back-button", style={
                'position': 'fixed',  # Position the button relative to the viewport
                'bottom': '10px',  # Distance from the bottom edge
                'left': '10px',  # Distance from the left edge
                'zIndex': '1000',  # Ensure it appears above other elements
                'backgroundColor': '#007bff',  # Optional: button color
                'color': 'white',  # Optional: text color
                'padding': '10px 20px',  # Optional: button padding
                'border': 'none',  # Optional: button border
                'borderRadius': '5px',  # Optional: rounded corners
                'cursor': 'pointer'  # Optional: pointer cursor on hover
            }),
            href="/"  # URL to navigate back to the root page
        )

    ], style={'display': 'flex', 'flexDirection': 'row', 'gap': '40px', 'width': '100%', 'maxWidth': '2000px',
              'margin': '0 auto'})
], style={'width': '190%'})

initial_treemap_fig = create_treemap()


@app.callback(
    [Output('url', 'pathname'), Output('treemap-graph', 'figure')],
    [Input('treemap-graph', 'clickData'), Input('autocomplete-dropdown', 'value')],
    [State('autocomplete-dropdown', 'value')]
)
def update_url_and_treemap(click_data, search_value, _):
    # Handle clickData first (for clicking on the treemap)
    if click_data:
        item_name = click_data['points'][0]['label']

        if item_name in treemap_df['Company'].values:
            return f'/item/{item_name}', dash.no_update
        elif item_name in treemap_df['Industry'].values:
            return '/', initial_treemap_fig

    # Handle search input when a value is selected or typed in
    if search_value:
        if search_value in nasdaq_df['Company'].values:
            return f'/item/{search_value}', dash.no_update
        elif search_value in nasdaq_df['Ticker'].values:
            company_name = nasdaq_df.loc[nasdaq_df['Ticker'] == search_value, 'Company'].values[0]
            return f'/item/{company_name}', dash.no_update

    # Default case (return to the root page with initial figure)
    return '/', initial_treemap_fig


@app.callback(
    [Output('page-content', 'children'),
     Output('sidebar', 'style')],  # Control sidebar visibility
    [Input('url', 'pathname'), Input('compare-button', 'value')]
)
def display_page(pathname, compare_value):
    if compare_value == 2 or pathname == '/compare':
        # Compare page layout and hide sidebar
        return compare_page_layout, {'display': 'none'}

    elif pathname.startswith('/item/'):
        # Extract the company name from the pathname
        company_name = pathname.split('/')[-1].replace('-', ' ').capitalize()

        # Get company summary dynamically
        company_summary = get_company_summary(company_name, treemap_df, nasdaq_df)

        # Summarize the company description if available
        if "not found" not in company_summary:
            company_summary = simple_summarizer(company_summary)

        return html.Div([
            html.H1(f"Details for {company_name}"),
            html.Br(),
            html.Div([
                html.H3("Company Summary"),
                html.P(company_summary, style={'fontSize': '16px', 'color': '#333'})
            ], style={'padding': '20px', 'border': '1px solid #ddd', 'borderRadius': '5px', 'backgroundColor': '#f9f9f9'}),
            html.Div([
                html.Label("Select Time Period:", style={'color': 'white'}),
                dcc.Dropdown(
                    id="time-period-dropdown",
                    options=[
                        {"label": "1 Day (1min interval)", "value": "1d"},
                        {"label": "5 Days (1d interval)", "value": "5d"},
                        {"label": "1 Month (1d interval)", "value": "1mo"},
                        {"label": "3 Months (1d interval)", "value": "3mo"},
                        {"label": "6 Months (1d interval)", "value": "6mo"},
                        {"label": "1 Year (1d interval)", "value": "1y"},
                        {"label": "5 Years (1d interval)", "value": "5y"},
                        {"label": "Max (1wk interval)", "value": "max"}
                    ],
                    value="1d",  
                    clearable=False,
                    style={'width': '200px'}
                    ),
    
    dcc.Graph(id="real-time-stock-graph", style={'height': '500px', 'width': '100%'}),
    
    # Interval component to refresh data
    dcc.Interval(id="interval-component", interval=5000, n_intervals=0)
]),
            dcc.Slider(
                id='year-dropdown',
                min=0,
                max=3,
                marks={i: year for i, year in enumerate(['2021', '2022', '2023', '2024'])},
                value=0,  # Default value corresponds to '2020'
                step=None
            ),

            # Top two graphs
            dbc.Row([
                dbc.Col(dcc.Graph(id='company-graphic', style={'height': '500px', 'width': '100%'}), width=6),
                dbc.Col(dcc.Graph(id='company-cashflow-graphic', style={'height': '500px', 'width': '100%'}), width=6)
            ], style={'width': '100%'}),

            # Bottom graph
            dbc.Row([
                dbc.Col(dcc.Graph(id='company-balance-graphic', style={'height': '500px', 'width': '100%'}), width=6),
                dbc.Col(dcc.Graph(id='equity-bond-graph', style={'height': '500px', 'width': '100%'}), width=6)
            ], style={'width': '100%'}),

            # Back Button
            html.A(
                html.Button("Back to Treemap", id="back-button", style={
                    'position': 'fixed',
                    'bottom': '10px',
                    'left': '10px',
                    'zIndex': '1000',
                    'backgroundColor': '#007bff',
                    'color': 'white',
                    'padding': '10px 20px',
                    'border': 'none',
                    'borderRadius': '5px',
                    'cursor': 'pointer'
                }),
                href="/"  # URL to navigate back to the root page
            )
        ], style={'width': '200%'}), {'display': 'none'}

    # Default to main page with sidebar
    return main_page_layout, {'width': 340, 'margin-left': 35, 'margin-top': 35}


# all code for the main page
@app.callback(
    Output('company-graphic', 'figure'),
    Output('company-graphic', 'style'),
    [Input('url', 'pathname'),
     Input('year-dropdown', 'value')]
)
def update_company_graphic(pathname, slider_value):
    # Define the list of years corresponding to slider indices
    years = ['2021', '2022', '2023', '2024']

    # Convert the slider numeric value to the corresponding year string
    selected_year = years[slider_value]

    # Extract the company name from the pathname
    company_name = pathname.split('/')[-1]

    if company_name in treemap_df['Company'].values:
        return generate_sankey(pathname, selected_year, treemap_df)
    else:
        return generate_sankey(pathname, selected_year, nasdaq_df)


@app.callback(
    Output('company-balance-graphic', 'figure'),
    [Input('url', 'pathname'),
     Input('year-dropdown', 'value')]
)
def update_company_graphic_balance(pathname, slider_value):
    # Define the list of years corresponding to slider indices
    years = ['2021', '2022', '2023', '2024']

    # Convert the slider numeric value to the corresponding year string
    selected_year = years[slider_value]

    # Extract the company name from the pathname
    company_name = pathname.split('/')[-1]

    if company_name in treemap_df['Company'].values:
        return generate_balance_visual(pathname, selected_year, treemap_df)
    else:
        return generate_balance_visual(pathname, selected_year, nasdaq_df)

@app.callback(
    Output("real-time-stock-graph", "figure"),
    [Input("url", "pathname"), Input("interval-component", "n_intervals"), Input("time-period-dropdown", "value")]
)
def update_real_time_stock_graph(pathname, n_intervals, selected_period):
    """Fetches and updates stock data based on the selected time period, ensuring correct intervals."""
    
    # Extract the company name from the pathname
    company_name = pathname.split('/')[-1]

    # Get the ticker symbol
    matched_tickers = treemap_df[treemap_df['Company'] == company_name]['Ticker']
    if matched_tickers.empty:
        return go.Figure()

    ticker = matched_tickers.values[0]

    # **Set interval based on selected period**
    if selected_period == "1d":
        selected_interval = "1m"  # 1-minute intervals for 1-day view
    elif selected_period == "max":
        selected_interval = "1wk"  # 1-week intervals for max period
    else:
        selected_interval = "1d"  # 1-day intervals for all other periods

    # Fetch stock data for selected period & interval
    stock = yf.Ticker(ticker)
    stock_data = stock.history(period=selected_period, interval=selected_interval)

    if stock_data.empty:
        return go.Figure()

    # Create the line chart for stock prices
    fig = go.Figure(go.Scatter(
        x=stock_data.index,
        y=stock_data['Close'],
        mode="lines",
        name=f"{ticker} Price",
        line=dict(color="cyan", width=2)
    ))

    # Layout improvements
    fig.update_layout(
        title=f"Stock Price: {company_name} ({ticker}) [{selected_period}]",
        xaxis_title="Date",
        yaxis_title="Stock Price (USD)",
        template="plotly_dark",
        paper_bgcolor="#121212",
        plot_bgcolor="#121212"
    )

    return fig

@app.callback(
    Output('company-cashflow-graphic', 'figure'),
    [Input('url', 'pathname'),
     Input('year-dropdown', 'value')]
)

def update_company_cash(pathname, slider_value):
    # Define the list of years corresponding to slider indices
    years = ['2021', '2022', '2023', '2024']

    # Convert the slider numeric value to the corresponding year string
    selected_year = years[slider_value]

    # Extract the company name from the pathname
    company_name = pathname.split('/')[-1]

    if company_name in treemap_df['Company'].values:
        return generate_cashflow_visual(pathname, selected_year, treemap_df)
    else:
        return generate_cashflow_visual(pathname, selected_year, nasdaq_df)

@app.callback(
    Output("equity-bond-graph", "figure"),
    [Input("url", "pathname"), Input("year-dropdown", "value")]
)
def update_equity_bond(pathname, slider_value):
    """Updates the Equity Bond Yield graph based on the selected company and year."""
    
    # Define the list of years corresponding to slider indices
    years = ['2021', '2022', '2023', '2024']
    
    # Convert the slider numeric value to the corresponding year string
    selected_year = years[slider_value]

    # Extract the company name from the pathname
    company_name = pathname.split('/')[-1]

    # Determine which dataset to use (S&P 500 or Nasdaq)
    if company_name in treemap_df['Company'].values:
        return generate_equity_bond(pathname, selected_year, treemap_df)
    else:
        return generate_equity_bond(pathname, selected_year, nasdaq_df)
    return go.Figure()




if __name__ == "__main__":

    app.run_server(debug=True, port=8060)



