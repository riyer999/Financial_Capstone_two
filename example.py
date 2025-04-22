# Extract values
operating_cash_flow = financial_metrics_all_years.get(f'Operating_Cash_Flow_{selected_year}', 0)
issuance_of_debt = financial_metrics_all_years.get(f'Issuance_Of_Debt_{selected_year}', 0)

# Prepare categories and values based on sign of operating cash flow
category1 = []
value1 = []
category2 = ['Capital Expenditure', 'Repayment Of Debt', 'Repurchase Of Capital Stock', 'Cash Dividends Paid']
value2 = [
    financial_metrics_all_years.get(f'Capital_Expenditure_{selected_year}', 0),
    financial_metrics_all_years.get(f'Repayment_Of_Debt_{selected_year}', 0),
    financial_metrics_all_years.get(f'Repurchase_Of_Capital_Stock_{selected_year}', 0),
    financial_metrics_all_years.get(f'Cash_Dividends_Paid_{selected_year}', 0)
]

# Add operating cash flow to the appropriate list
if operating_cash_flow >= 0:
    category1.append('Operating Cash Flow')
    value1.append(operating_cash_flow)
else:
    category2.append('Operating Cash Flow')
    value2.append(abs(operating_cash_flow))  # Flip sign for display

# Always include Issuance of Debt in Money In
category1.append('Issuance Of Debt')
value1.append(issuance_of_debt)

# Prepare final data dictionary
year_data = {
    'Year': selected_year,
    'Category1': category1,
    'Value1': value1,
    'Category2': category2,
    'Value2': value2
}
