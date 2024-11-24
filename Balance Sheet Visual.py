import pickle
import plotly.express as px
import pandas as pd

company = 'KO'
date = '2020'

# Function to load the financial data from the pickle file
def load_data(ticker, year):
    with open('allData.pkl', 'rb') as file:  # Dictionary with the financial data information
        allData = pickle.load(file)

    balance_sheet = allData[ticker]['balance_sheet']
    pd.set_option('display.max_rows', None)  # None displays all rows
    pd.set_option('display.max_columns', None)  # None displays all columns
    print(balance_sheet)

    # List of keys to extract from the balance sheet
    keys = [
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

    variable_names = {}
    for key in keys:
        # Check if the key exists in the balance sheet index, else default to 0
        variable_names[key.replace(" ", "_")] = (
            balance_sheet.loc[key, year].item() if key in balance_sheet.index else 0
        )

    return variable_names  # Return the dictionary with variable names and values

# Load the financial data
financial_metrics = load_data(company, date)

# Create a hierarchical representation for the treemap
# Create a hierarchical representation for the treemap
data = {
    "category": [],
    "subcategory": [],
    "type": [],  # New hierarchy level
    "item": [],
    "value": []
}

# Define hierarchy for treemap, adding a "type" level for demonstration
hierarchy = {
    "Total Assets": {
        "Current Assets": {
            "Cash Cash Equivalents And Short Term Investments": [
                "Cash And Cash Equivalents",
                "Other Short Term Investments"
            ],
            "Receivables": [
                "Receivables",
            ],
            "Inventory":[
                "Raw Materials",
                "Finished Goods",
                "Other Inventories",
            ],
            "Prepaid Assets": [
                "Prepaid Assets",
            ],
            "Other Current Assets": [
                "Other Current Assets",
            ]
        },
        "Total Non-current Assets": {
            "Net PPE": [
                "Net PPE",
            ],
            "Goodwill And Other Intangible Assets": [
                "Goodwill",
                "Other Intangible Assets",
            ],
            "Investments And Advances": [
                "Long Term Equity Investment",
                "Other Investments"
            ],
            "Non Current Accounts Receivable": [
                "Non Current Accounts Receivable",
            ],
            "Non Current Note Receivables": [
                "Non Current Note Receivables",
            ],
            "Non Current Deferred Assets": [
                "Non Current Deferred Assets",
            ],
            "Defined Pension Benefit": [
                "Defined Pension Benefit",
            ],
            "Other Non Current Assets": [
                "Other Non Current Assets",
            ]
        }
    },
    "Total Liabilities and Equity": {
        "Total Liabilities Net Minority Interest": {
            "Current Liabilities": [
                "Payables And Accrued Expenses",
                "Pensionand Other Post Retirement Benefit Plans ...",
                "Current Debt And Capital Lease Obligation",
                "Other Current Liabilities"
            ],
            "Total Non Current Liabilities Net Minority Interest": [
                "Long Term Debt And Capital Lease Obligation",
                "Non Current Deferred Liabilities",
                "Other Non Current Liabilities"
            ]


        },
        "Total Equity Gross Minority Interest": {
            "Stockholders Equity": [  #something is wrong with the yahoo finances chart for stockholder's equity
                "Stockholders Equity" 
            ],
            "Minority Interest": [
                "Minority Interest"
            ]
        }
    }
}

# Build data dynamically based on the hierarchy
for category, subcategories in hierarchy.items():
    for subcategory, types in subcategories.items():
        for type_, items in types.items():
            for item in items:
                # Add item to treemap data
                data["category"].append(category)
                data["subcategory"].append(subcategory)
                data["type"].append(type_)  # Add the new hierarchy level
                data["item"].append(item)
                data["value"].append(financial_metrics.get(item.replace(" ", "_"), 0))

# Create the treemap
balance_fig = px.treemap(data, path=['category', 'subcategory', 'type', 'item'], values='value')  # Include new level in path
balance_fig.update_layout(margin=dict(t=50, l=400, r=400, b=25))
balance_fig.update_traces(maxdepth=2)  # Update maxdepth to account for the additional hierarchy level

# Show the plot
balance_fig.show()


##so i am kinda close but the issue is that i need to be able to return 3 values when i am only returning 2 right with the callback

#troubleshooting og code

@app.callback(
    [Output("graph1", "figure"), Output("balance-graph-1", "figure"), Output("graph1-container", "style"), Output("balance-graph-1-container", "style")],
    [Input("autocomplete-dropdown1", "value"), Input("year-dropdown-1", "value")]
)
def update_graph1(company_name, selected_year):
    return generate_graph(company_name, selected_year)

@app.callback(
    [Output("graph2", "figure"), Output("balance-graph-2", "figure"), Output("graph2-container", "style"), Output("balance-graph-2-container", "style")],
    [Input("autocomplete-dropdown2", "value"), Input("year-dropdown-2", "value")]
)
def update_graph2(company_name, selected_year):
    return generate_graph(company_name, selected_year)


def generate_graph(company_name, selected_year):
    if not company_name or not selected_year:
        return {}, {}, {'display': 'none'}, {'display': 'none'}
    if company_name or selected_year:
        print(f"Displaying details for {company_name}")  # Debugging

        # Normalize company name to match entries in your DataFrame
        company_name_normalized = company_name.strip().lower()

        # Assuming you have a 'Normalized_Company' column for matching in `treemap_df`
        treemap_df['Normalized_Company'] = treemap_df['Company'].str.strip().str.lower()

        # Get the ticker corresponding to the company
        matched_tickers = treemap_df[treemap_df['Normalized_Company'] == company_name_normalized]['Ticker']
        print(f"Matched tickers: {matched_tickers}")  # Debugging

        if not matched_tickers.empty:
            ticker = matched_tickers.values[0]
            print(f"Selected ticker: {ticker}")  # Debugging
            # Load financial data for the selected company
            financial_metrics = load_data(ticker, years=[selected_year])  # Load data for the specific year
            print(financial_metrics.keys())
            if financial_metrics:

                # Extract the financial metrics you need
                total_revenue = financial_metrics[f'Total_Revenue_{selected_year}'] / 1e9
                gross_profit_value = financial_metrics[f'Gross_Profit_{selected_year}'] / 1e9
                cost_revenue = financial_metrics[f'Cost_Of_Revenue_{selected_year}'] / 1e9
                operating_income = financial_metrics[f'Operating_Income_{selected_year}'] / 1e9
                operating_expense = financial_metrics[f'Operating_Expense_{selected_year}'] / 1e9
                tax_provision = financial_metrics[f'Tax_Provision_{selected_year}'] / 1e9
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
                value = [gross_profit_value, cost_revenue, operating_income, operating_expense, net_income,
                         tax_provision, other, sga, other_operating_expenses]

                link = dict(source=source, target=target, value=value, color=color_link)
                node = dict(label=label, pad=35, thickness=20)
                data = go.Sankey(link=link, node=node)

                # Coordinates for nodes
                x = [0.1, 0.35, 0.35, 0.6,
                     0.6, 0.85, 0.85, 0.85, 0.85, 0.85]
                y = [0.40, 0.25, 0.70, 0.1,
                     0.45, 0.0, 0.15, 0.30, 0.45, 0.60]
                x = [.001 if v == 0 else .999 if v == 1 else v for v in x]
                y = [.001 if v == 0 else .999 if v == 1 else v for v in y]

                sankey_fig = go.Figure(data=[go.Sankey(
                    textfont=dict(color="black", size=10),
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
                    title_text="Market Cap and Income Statement Sankey",
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

                #################### balance sheet
                data = {
                    "category": [],
                    "subcategory": [],
                    "type": [],
                    "item": [],
                    "value": []
                }

                # Define hierarchy for treemap
                hierarchy = {
                    "Total Assets": {
                        "Current Assets": {
                            "Cash Cash Equivalents And Short Term Investments": [
                                "Cash And Cash Equivalents",
                                "Other Short Term Investments"
                            ],
                            "Receivables": [
                                "Receivables",
                            ],
                            "Inventory": [
                                "Raw Materials",
                                "Finished Goods",
                                "Other Inventories",
                            ],
                            "Prepaid Assets": [
                                "Prepaid Assets",
                            ],
                            "Other Current Assets": [
                                "Other Current Assets",
                            ]
                        },
                        "Total Non-current Assets": {
                            "Net PPE": [
                                "Net PPE",
                            ],
                            "Goodwill And Other Intangible Assets": [
                                "Goodwill",
                                "Other Intangible Assets",
                            ],
                            "Investments And Advances": [
                                "Long Term Equity Investment",
                                "Other Investments"
                            ],
                            "Non Current Accounts Receivable": [
                                "Non Current Accounts Receivable",
                            ],
                            "Non Current Note Receivables": [
                                "Non Current Note Receivables",
                            ],
                            "Non Current Deferred Assets": [
                                "Non Current Deferred Assets",
                            ],
                            "Defined Pension Benefit": [
                                "Defined Pension Benefit",
                            ],
                            "Other Non Current Assets": [
                                "Other Non Current Assets",
                            ]
                        }
                    },
                    "Total Liabilities and Equity": {
                        "Total Liabilities Net Minority Interest": {
                            "Current Liabilities": [
                                "Payables And Accrued Expenses",
                                "Pensionand Other Post Retirement Benefit Plans ...",
                                "Current Debt And Capital Lease Obligation",
                                "Other Current Liabilities"
                            ],
                            "Total Non Current Liabilities Net Minority Interest": [
                                "Long Term Debt And Capital Lease Obligation",
                                "Non Current Deferred Liabilities",
                                "Other Non Current Liabilities"
                            ]
                        },
                        "Total Equity Gross Minority Interest": {
                            "Stockholders Equity": [
                                "Stockholders Equity"
                            ],
                            "Minority Interest": [
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
                                value = financial_metrics.get(metric_key,
                                                              0) / 1e9  # Convert to billions for visualization

                                # Append data for treemap
                                data["category"].append(category)
                                data["subcategory"].append(subcategory)
                                data["type"].append(type_)
                                data["item"].append(item)
                                data["value"].append(value)

                # Create the treemap
                balance_fig = px.treemap(
                    data,
                    path=['category', 'subcategory', 'type', 'item'],  # Include all hierarchy levels
                    values='value'
                )
                balance_fig.update_layout(margin=dict(t=50, l=400, r=400, b=25), font=dict(size=23))
                balance_fig.update_traces(maxdepth=2)  # Adjust maxdepth for the full hierarchy
                fig.show()

                # Show the plot
                balance_fig.show()



                return fig, balance_fig, {'display': 'block'}, {'display': 'block'}




compare_page_layout = html.Div([
    html.H1("Compare Companies"),
    html.P("Here you can compare different companies."),

    # Wrapper for the two columns
    html.Div([

        # Column for Company 1
        html.Div([
            html.Div([
                html.Label("Company 1 Search"),
                dcc.Dropdown(
                    id="autocomplete-dropdown1",
                    options=autocomplete_options1,
                    placeholder="Enter Company 1 Name or Ticker",
                    style={'width': 200, 'backgroundColor': '#333333', 'color': '#000000'},
                    searchable=True,
                    multi=False,
                ),
            ], style={'padding': '10px'}),

            html.Div([
                html.Label("Select Year"),
                dcc.Dropdown(
                    id="year-dropdown-1",
                    options=[{"label": str(year), "value": str(year)} for year in range(2020, 2024)],
                    placeholder="Select Year"
                ),
            ], style={'padding': '10px'}),

            html.Div([
                dcc.Graph(id="graph1", style={'width': '100%', 'height': '50vh'}),
            ], id="graph1-container", style={'padding': '10px', 'display': 'block'}),

            # Balance Graph for Company 1 (container added back)
            html.Div([
                dcc.Graph(id="balance-graph-1", style={'width': '100%', 'height': '50vh'}),
            ], id="balance-graph-1-container", style={'padding': '10px', 'display': 'block'}),  # Container for balance graph
        ], style={'flex': '2', 'padding': '10px', 'border': '1px solid #ccc'}),

        # Column for Company 2
        html.Div([
            html.Div([
                html.Label("Company 2 Search"),
                dcc.Dropdown(
                    id="autocomplete-dropdown2",
                    options=autocomplete_options1,
                    placeholder="Enter Company 2 Name or Ticker",
                    style={'width': 200, 'backgroundColor': '#333333', 'color': '#932182'},
                    searchable=True,
                    multi=False,
                ),
            ], style={'padding': '10px'}),

            html.Div([
                html.Label("Select Year"),
                dcc.Dropdown(
                    id="year-dropdown-2",
                    options=[{"label": str(year), "value": str(year)} for year in range(2020, 2024)],
                    placeholder="Select Year"
                ),
            ], style={'padding': '10px'}),

            html.Div([
                dcc.Graph(id="graph2", style={'width': '100%', 'height': '50vh'}),
            ], id="graph2-container", style={'padding': '10px', 'display': 'block'}),

            # Balance Graph for Company 2 (container added back)
            html.Div([
                dcc.Graph(id="balance-graph-2", style={'width': '100%', 'height': '50vh'}),
            ], id="balance-graph-2-container", style={'padding': '10px', 'display': 'block'}),  # Container for balance graph
        ], style={'flex': '2', 'padding': '10px', 'border': '1px solid #ccc'}),

    ], style={'display': 'flex', 'flexDirection': 'row', 'gap': '40px', 'width': '100%', 'maxWidth': '2000px',
              'margin': '0 auto'})
], style={'width': '190%'})