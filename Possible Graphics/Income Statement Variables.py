import pickle

ticker = 'KO'
year = '2023'

def load_data(ticker, year):  # Loads the financial data.
    with open('allData.pkl', 'rb') as file:  # Dictionary with the financial data information
        allData = pickle.load(file)

    income_statement = allData[ticker]['income_statement']
    print(income_statement)

    # List of keys to extract from the income statement
    keys = [
      #  'Tax Effect Of Unusual Items',
      #  'Tax Rate For Calcs',
       # 'Normalized EBITDA',
        'Total Unusual Items',
        'Total Unusual Items Excluding Goodwill',
      #  'Reconciled Depreciation',
        #'Reconciled Cost Of Revenue',
       # 'EBITDA',
       # 'EBIT',
        'Net Interest Income',
        'Interest Expense',
        'Interest Income',
        'Normalized Income',
     #   'Total Expenses',
        'Total Operating Income As Reported',
     #   'Diluted Average Shares',
        'Basic Average Shares',
     #   'Diluted EPS',
    #    'Basic EPS',
        #'Diluted NI Availto Com Stockholders',
        #'Net Income Common Stockholders',
        'Net Income',
        'Minority Interests',
        'Net Income Including Noncontrolling Interests',
        'Net Income Continuous Operations',
        'Tax Provision',
        'Pretax Income',
        'Other Income Expense',
       # 'Other Non Operating Income Expenses',
        #'Special Income Charges',
       # 'Write Off',
        'Impairment Of Capital Assets',

        #'Earnings From Equity Interest',
        #'Gain On Sale Of Security',
        'Net Non Operating Interest Income Expense',
        'Interest Expense Non Operating',
        #'Interest Income Non Operating',
        'Operating Income',
        'Operating Expense',
       # 'Other Operating Expenses',
      #  'Depreciation Amortization Depletion Income Statement',
       # 'Depreciation And Amortization In Income Statement',
        #'Amortization',
        #'Amortization Of Intangibles Income Statement',
        'Selling General And Administration',
        #'General And Administrative Expense',
        #'Selling And Marketing Expense',
        #'General And Administrative Expense',
        #'Other Gand A',
        #'Salaries And Wages',
        'Gross Profit',
        'Cost Of Revenue',
        'Total Revenue',
        'Operating Revenue'
    ]

    # Create a dictionary to hold variable names and their corresponding values
    variable_names = {key.replace(" ", "_"): income_statement.loc[key, year].item() for key in keys}

    return variable_names  # Return the dictionary with variable names and values

# Load the financial data
financial_metrics = load_data(ticker, year)

# Access the Total Revenue
print(financial_metrics['Total_Revenue']/1000000000)
print(financial_metrics['Gross_Profit']/1000000000)
print(financial_metrics['Cost_Of_Revenue']/1000000000)
#financial_metrics['General And Administrative Expense']/1000000000
#financial_metrics['Selling And Marketing Expense']/1000000000

