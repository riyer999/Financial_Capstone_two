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
fig = px.treemap(data, path=['category', 'subcategory', 'type', 'item'], values='value')  # Include new level in path
fig.update_layout(margin=dict(t=50, l=400, r=400, b=25))
fig.update_traces(maxdepth=2)  # Update maxdepth to account for the additional hierarchy level

# Show the plot
fig.show()

