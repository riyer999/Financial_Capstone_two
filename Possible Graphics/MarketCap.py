import plotly.graph_objects as go
import pandas as pd

# Example data
data = {
    'Category': [''],  # Only one category (company)
    'Net Profit': [13.9],
    'Market Cap': [210.2],
    'Revenue': [55.2],        # Market Cap (in Billion)
                    # Net Profit (in Billion)
}

df = pd.DataFrame(data)

# Create a stacked bar chart with a hidden second segment
fig = go.Figure(data=[

    go.Bar(
        name='Net Profit', 
        x=df['Category'], 
        y=df['Net Profit'], 
        marker_color='green',  # White to make it invisible
        text=['Net Profit: 13.9'],  # This will not be visible due to the white color
        textposition='inside',
        textfont=dict(color='white')  # Making the text white as well, so it's invisible
    ),
    # Market Cap (Visible)
    go.Bar(
        name='Market Cap', 
        x=df['Category'], 
        y=df['Revenue'], 
        marker_color='steelblue',  # Color for Market Cap
        text=['Revenue: 69.1'],  # Show value for Market Cap
        textposition='inside',  # Text inside the bar
        textfont=dict(color='white')  # Text color white
    ),
    go.Bar(
        name='Market Cap', 
        x=df['Category'], 
        y=df['Market Cap'], 
        marker_color='steelblue',  # Color for Market Cap
        text=['Market Cap: 293.2'],  # Show value for Market Cap
        textposition='inside',  # Text inside the bar
        textfont=dict(color='white')  # Text color white
    ),
    
    # Net Profit (Hidden but still part of the stack)
    
])

# Update layout for stacking and appearance
fig.update_layout(
    barmode='stack',  # Stack bars
    title='Market Cap Proportionality',  # Title
    xaxis_title='',  # X-axis title
    yaxis_title='Amount (in Billions)',  # Y-axis title
    showlegend=False  # Hide the legend (since you don't need to see Net Profit)
)

fig.show()