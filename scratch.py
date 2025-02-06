def generate_balance_visual(company, selected_year, company_dataframe):
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
        print(f"Selected ticker: {ticker}")
        financial_metrics = load_data(ticker, years=[selected_year])  # Load data for the specific year

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
                "Total Liabilities": {
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
                "Total Equity": {
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
                        value = financial_metrics.get(metric_key, 0) / 1e9  # Convert to billions for visualization

                        # Append data for treemap
                        data["root"].append("Balance Sheet")  # Add root node
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
            maxdepth=3,  # Adjust depth to include all levels
            hovertemplate='<b>%{label}</b><br>%{value} Billion<extra></extra>',
            textfont=dict(size=23)  # Adjust the font size
        )

        # Update layout
        balance_fig.update_layout(
            margin=dict(t=50, l=50, r=50, b=50)
        )

        # Show the plot
        #balance_fig.show()
        return balance_fig