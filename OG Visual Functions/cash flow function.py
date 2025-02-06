
def generate_cashflow_visual(company, selected_year, company_dataframe):
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

#########################
def generate_cashflow_visual(company, selected_year, company_dataframe):
    if (company and selected_year) or (company and company.startswith('/item/')):
        # Determine the correct company name
        company_name = company.split('/')[-1] if company.startswith('/item/') else company
        print(f"Displaying details for {company_name}")  # Debugging

        # Normalize company name to match entries in DataFrame
        company_name_normalized = company_name.strip().lower()
        company_dataframe['Normalized_Company'] = company_dataframe['Company'].str.strip().str.lower()

        # Get the ticker corresponding to the company
        matched_tickers = company_dataframe[company_dataframe['Normalized_Company'] == company_name_normalized][
            'Ticker']
        print(f"Matched tickers: {matched_tickers}")  # Debugging

    if not matched_tickers.empty:
        ticker = matched_tickers.values[0]
        print(f"Selected ticker: {ticker}")
        financial_metrics = load_data(ticker, years=[selected_year])  # Load data for the specific year

        # Prepare DataFrame for Plotly
        plot_data = []
        max_value = 0  # Initialize the max value tracker

        year_data = {
            'Year': selected_year,
            'Category1': ['Operating Cash Flow', 'Issuance Of Debt'],
            'Value1': [
                financial_metrics.get(f'Operating_Cash_Flow_{selected_year}', 0),
                financial_metrics.get(f'Issuance_Of_Debt_{selected_year}', 0)
            ],
            'Category2': ['Capital Expenditure', 'Repayment Of Debt', 'Repurchase Of Capital Stock'],
            'Value2': [
                financial_metrics.get(f'Capital_Expenditure_{selected_year}', 0),
                financial_metrics.get(f'Repayment_Of_Debt_{selected_year}', 0),
                financial_metrics.get(f'Repurchase_Of_Capital_Stock_{selected_year}', 0)
            ]
        }
        plot_data.append(year_data)
        max_value = max(max_value, *year_data['Value1'], *year_data['Value2'])

        # Create subplots
        cash_fig = make_subplots(rows=1, cols=2, subplot_titles=("Money In", "Money Out"))

        # Add traces
        cash_fig.add_trace(go.Bar(
            x=year_data['Category1'],
            y=year_data['Value1'],
            name=f'Year {year_data["Year"]} - Money In',
            marker=dict(color='green')
        ), row=1, col=1)

        cash_fig.add_trace(go.Bar(
            x=year_data['Category2'],
            y=year_data['Value2'],
            name=f'Year {year_data["Year"]} - Money Out',
            marker=dict(color='red')
        ), row=1, col=2)

        # Update layout
        cash_fig.update_layout(
            title_text=f"Cash Flow for {ticker}",
            xaxis_title="",
            yaxis_title="Money in Billions of Dollars",
            showlegend=False,
            xaxis=dict(
                tickmode='array',
                tickvals=['Operating Cash Flow', 'Issuance Of Debt', 'Capital Expenditure', 'Repayment Of Debt',
                          'Repurchase Of Capital Stock'],
                ticktext=['Operating Cash Flow', 'Issuance Of Debt', 'Capital Expenditure', 'Repayment Of Debt',
                          'Repurchase Of Capital Stock']
            ),
            yaxis=dict(range=[0, max_value * 1.1]),
            yaxis2=dict(range=[0, max_value * 1.1])
        )

        # Show plot
        cash_fig.show()
        return cash_fig
