import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


# Function to load data dynamically
def load_data(ticker, years=['2020', '2021', '2022', '2023', '2024']):
    # Fetch the data dynamically using yfinance
    ystock = yf.Ticker(ticker)

    # Fetch the financial data
    cashflow_statement = ystock.cashflow  # This fetches the cash flow statement

    cashflow_statement_keys = {
        'Operating Cash Flow',
        'Issuance Of Debt',
        'Capital Expenditure',
        'Repayment Of Debt',
        'Repurchase Of Capital Stock',
    }

    variable_names = {}

    # loop through the years and each key for the cash flow statement
    for year in years:
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


# Load actual data
ticker = "KO"
years = ['2020', '2021', '2022', '2023', '2024']
data = load_data(ticker, years)

# Prepare DataFrame for Plotly
plot_data = []
max_value = 0  # Initialize the max value tracker

# Prepare the data for plotting and calculate the maximum value
for year in years:
    year_data = {
        'Year': year,
        'Category1': ['Operating Cash Flow', 'Issuance Of Debt'],
        'Value1': [data.get(f'Operating_Cash_Flow_{year}', 0), data.get(f'Issuance_Of_Debt_{year}', 0)],
        'Category2': ['Capital Expenditure', 'Repayment Of Debt', 'Repurchase Of Capital Stock'],
        'Value2': [
            data.get(f'Capital_Expenditure_{year}', 0),
            data.get(f'Repayment_Of_Debt_{year}', 0),
            data.get(f'Repurchase_Of_Capital_Stock_{year}', 0)
        ]
    }
    plot_data.append(year_data)

    # Track the maximum value for y-axis scaling
    max_value = max(max_value, *year_data['Value1'], *year_data['Value2'])

# Create subplots
fig = make_subplots(rows=1, cols=2, subplot_titles=("Money In", "Money Out"))

# Add traces
for i, year_data in enumerate(plot_data):
    fig.add_trace(go.Bar(
        x=year_data['Category1'],
        y=year_data['Value1'],
        name=f'Year {year_data["Year"]} - Money In',
        marker=dict(color='green'),
        visible=(i == 0)
    ), row=1, col=1)

    fig.add_trace(go.Bar(
        x=year_data['Category2'],
        y=year_data['Value2'],
        name=f'Year {year_data["Year"]} - Money Out',
        marker=dict(color='red'),
        visible=(i == 0)
    ), row=1, col=2)

# Slider steps
steps = []
for i, year_data in enumerate(plot_data):
    step = {
        'method': 'update',
        'label': year_data['Year'],
        'args': [{'visible': [False] * len(fig.data)}]
    }
    step['args'][0]['visible'][i * 2] = True
    step['args'][0]['visible'][i * 2 + 1] = True
    steps.append(step)

# Add slider
fig.update_layout(
    sliders=[{
        'active': 0,
        'currentvalue': {'prefix': 'Year: '},
        'steps': steps
    }],
    title_text=f"Cash Flow for {ticker}",
    xaxis_title="",
    yaxis_title="Money in Billions of Dollars",
    showlegend=False,
    xaxis=dict(
        tickmode='array',  # To keep categories fixed on x-axis
        tickvals=['Operating Cash Flow', 'Issuance Of Debt', 'Capital Expenditure', 'Repayment Of Debt',
                  'Repurchase Of Capital Stock'],
        ticktext=['Operating Cash Flow', 'Issuance Of Debt', 'Capital Expenditure', 'Repayment Of Debt',
                  'Repurchase Of Capital Stock']
    ),
    yaxis=dict(
        range=[0, max_value * 1.1]  # Set y-axis range to the largest value, with a 10% margin
    ),
    yaxis2=dict(
        range=[0, max_value * 1.1],  # Set y-axis range for the second subplot as well
    ),
)

# Show plot
fig.show()
