import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd

# Sample data (multiple years)
data = {
    'Year': [2020, 2020, 2020, 2020, 2021, 2021, 2021, 2021, 2022, 2022, 2022, 2022, 2023, 2023, 2023, 2023],
    'Category1': ['Revenue', 'Loans', 'C', 'D', 'Revenue', 'Loans', 'C', 'D', 'Revenue', 'Loans', 'C', 'D', 'Revenue', 'Loans', 'C', 'D'],
    'Category2': ['Cap Ex', 'Debt Repay', 'Stock BB', 'Other', 'Cap Ex', 'Debt Repay', 'Stock BB', 'Other', 'Cap Ex', 'Debt Repay', 'Stock BB', 'Other', 'Cap Ex', 'Debt Repay', 'Stock BB', 'Other'],
    'Value1': [20, 5, 0, 0, 17, 3, 0, 0, 18, 2, 0, 0, 20, 4, 0, 0],  # First chart
    'Value2': [5, 10, 1, 0, 6, 9, 2, 1, 8, 5, 1, 0, 7, 5, 1, 0]    # Second chart
}

df = pd.DataFrame(data)
years = df['Year'].unique()

y1_min, y1_max = 0, df["Value1"].max() + 5  # Add padding for better visibility
y2_min, y2_max = 0, df["Value1"].max() + 5  # Add padding for better visibility

# Create subplots: 1 row, 2 columns
fig = make_subplots(rows=1, cols=2, subplot_titles=("Money In", "Money Out"))

# Add traces for each year
for year in years:
    df_year = df[df['Year'] == year]
    
    # First bar chart (left)
    fig.add_trace(go.Bar(
        x=df_year['Category1'],
        y=df_year['Value1'],
        name=f'Year {year} - Money In',
        marker=dict(color='green'),  # Set bar color to green
        visible=(year == years[0])  # Show only the first year initially
    ), row=1, col=1)
    
    # Second bar chart (right)
    fig.add_trace(go.Bar(
        x=df_year['Category2'],
        y=df_year['Value2'],
        name=f'Year {year} - Money Out',
        marker=dict(color='red'),  # Set bar color to green
        visible=(year == years[0])
    ), row=1, col=2)

# Create slider steps
steps = []
for i, year in enumerate(years):
    step = {
        'method': 'update',
        'label': str(year),
        'args': [
            {'visible': [False] * len(fig.data)}  # Hide all traces initially
        ]
    }
    step['args'][0]['visible'][i * 2] = True  # Show first chart for the selected year
    step['args'][0]['visible'][i * 2 + 1] = True  # Show second chart for the selected year
    steps.append(step)

# Add slider
fig.update_layout(
    sliders=[{
        'active': 0,
        'currentvalue': {'prefix': 'Year: '},
        'steps': steps
    }],
    title_text="Cash Flow",
    xaxis_title="",
    yaxis_title="Money in Billions of Dollars",
    showlegend=False
)
fig.update_yaxes(range=[y1_min, y1_max], row=1, col=1)  # Keep Y-axis fixed for "Money In"
fig.update_yaxes(range=[y2_min, y2_max], row=1, col=2)  # Keep Y-axis fixed for "Money Out"

# Show plot
fig.show()



