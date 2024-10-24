import plotly.graph_objects as go
import pickle

# Define the years for which data will be displayed
years = ['2020', '2021', '2022', '2023']
ticker = 'KO'


def load_data(ticker, year):
    # Load the financial data for a specific year
    with open('allData.pkl', 'rb') as file:
        allData = pickle.load(file)

    income_statement = allData[ticker]['income_statement']

    # List of keys to extract from the income statement
    keys = [
        'Total Revenue', 'Gross Profit', 'Cost Of Revenue',
        'Operating Income', 'Operating Expense',
        'Selling General And Administration', 'Net Income',
        'Tax Provision', 'Interest Expense Non Operating', 'Operating Revenue'
    ]

    # Create a dictionary with the values for the given year
    variable_names = {key.replace(" ", "_"): income_statement.loc[key, year].item() for key in keys}
    return variable_names


# Load financial data for all years
financial_data = {year: load_data(ticker, year) for year in years}


# Function to extract financial metrics for each year
def extract_metrics(year):
    data = financial_data[year]
    metrics = {
        'total_revenue': data['Total_Revenue'] / 1e9,
        'gross_profit': data['Gross_Profit'] / 1e9,
        'cost_of_revenue': data['Cost_Of_Revenue'] / 1e9,
        'operating_income': data['Operating_Income'] / 1e9,
        'operating_expense': data['Operating_Expense'] / 1e9,
        'tax_provision': data['Tax_Provision'] / 1e9,
        'sga': data['Selling_General_And_Administration'] / 1e9,
        'net_income': data['Net_Income'] / 1e9,
        'interest_expense': data['Interest_Expense_Non_Operating'] / 1e9,
    }
    return metrics


# Prepare the Sankey diagram for each year
data_by_year = {}
for year in years:
    metrics = extract_metrics(year)
    operating_profit = metrics['total_revenue'] - metrics['operating_expense']

    data_by_year[year] = dict(
        values=[metrics['total_revenue'], metrics['gross_profit'], metrics['cost_of_revenue'],
                metrics['sga'], operating_profit, metrics['net_income'],
                metrics['tax_provision'], metrics['interest_expense']],
        labels=['Total Revenue', 'Gross Profit', 'Cost of Goods Sold',
                'Selling, General, and Admin', 'Operating Profit',
                'Net Income', 'Tax Provision', 'Interest Expense'],
        source=[0, 1, 1, 2, 2, 2, 5, 5],
        target=[1, 2, 3, 4, 5, 6, 7, 8]
    )

# Define the initial data (for 2023) to display when the figure first loads
initial_year = '2023'
initial_data = data_by_year[initial_year]

# Create the initial Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=100,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=initial_data['labels']
    ),
    link=dict(
        source=initial_data['source'],  # Indices of the source nodes
        target=initial_data['target'],  # Indices of the target nodes
        value=initial_data['values'],  # Values for the flows
        color=['gray', 'green', 'red', 'red', 'green', 'red', 'green', 'red']
    )
)])

# Define the slider to control the year
sliders = [dict(
    active=3,  # Default to the latest year (2023)
    currentvalue={"prefix": "Year: "},
    pad={"t": 50},
    steps=[dict(label=year, method="update",
                args=[{"link.value": [data_by_year[year]['values']],
                       "node.label": [data_by_year[year]['labels']],
                       "link.source": [data_by_year[year]['source']],
                       "link.target": [data_by_year[year]['target']]}]) for year in years]
)]

# Update the layout with the slider
fig.update_layout(
    title_text="Sankey Diagram for Coca-Cola (KO)",
    font_size=10,
    sliders=sliders
)

# Show the figure
fig.show()
