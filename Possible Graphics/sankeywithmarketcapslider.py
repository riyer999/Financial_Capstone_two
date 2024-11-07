import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Initialize bar chart and Sankey diagram

# Bar chart trace
bar_fig = go.Figure()

# Market cap data
categories = ['Market Capitalization']
values = [293.2]  # in billions

# Bar chart with hover template
bar_fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color='steelblue',
    text=f"{values[0]}B",  # Display value in billions on the bar
    textposition='auto'  # Place the value on the bar
))

# Update layout for bar chart
bar_fig.update_layout(
    title='Market Capitalization Overview (FY23)',
    xaxis_title='Metric',
    yaxis_title='Market Cap (in Billions of USD)',
    paper_bgcolor='#F8F8FF'
)

# Custom hover label for the bar chart
bar_fig.update_traces(
    hovertemplate='Market Cap: %{y}B USD',
    selector=dict(type='bar')
)

# Data for the Sankey diagram
label = ['Revenue ($B)', 'Gross Profit ($B)', 'Cost of Revenues ($B)', 
         'Operating Profit ($B)', 'Operating Expenses ($B)', 'TAC ($B)', 
         'Others ($B)', 'Net Profit ($B)', 'Tax ($B)', 'Other ($B)', 
         'R&D ($B)', 'S&M ($B)', 'G&A ($B)']
source = [0, 0, 1, 1, 2, 2, 3, 3, 3, 4, 4, 4]
target = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
value = [37.9, 31.2, 17.1, 20.8, 11.8, 19.3, 13.9, 2.3, 0.9, 10.3, 6.9, 3.6]

# Sankey trace with `hoverinfo` and `valuesuffix`
sankey_fig = go.Figure(data=[go.Sankey(
    domain=dict(
        x=[0.1, 1.0],  # Adjust x to start slightly right, proportional to bar chart width
        y=[0.05, 0.95]
    ),
    node=dict(
        pad=35,
        thickness=20,
        label=label,
        color=['#4CAF50', '#4CAF50', '#FF6F61', '#4CAF50', '#FF6F61', 
               '#FF6F61', '#FF6F61', '#4CAF50', '#FF6F61', '#FF6F61', 
               '#FF6F61', '#FF6F61', '#FF6F61'],
        hoverlabel=dict(bgcolor="white", font_size=12)  # Customize hover label
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
        color=['#90EE90', '#FFB6C1', '#90EE90', '#FFB6C1', '#FFB6C1', 
               '#FFB6C1', '#90EE90', '#FFB6C1', '#FFB6C1', '#FFB6C1', 
               '#FFB6C1', '#FFB6C1'],
        hoverlabel=dict(bgcolor="white", font_size=12)  # Customize link hover label
    ),
    valueformat=".1f",
    valuesuffix="B USD",
    hoverinfo="all"  # Shows label and value
)])

sankey_fig.update_layout(
    hovermode='x',
    title="Coca-Cola FY23 Income Flow Breakdown",
    font=dict(size=10, color='black'),
    paper_bgcolor='#F8F8FF'
)

# Create subplot with bar chart and Sankey diagram
fig = make_subplots(
    rows=1, cols=2,
    column_widths=[0.05, 0.95],
    specs=[[{"type": "bar"}, {"type": "sankey"}]]
)

# Add bar chart data to subplot
for trace in bar_fig.data:
    fig.add_trace(trace, row=1, col=1)

# Add Sankey data to subplot
for trace in sankey_fig.data:
    fig.add_trace(trace, row=1, col=2)

# Main title for combined plot
fig.update_layout(
    title_text="Market Cap and Financial Breakdown",
    paper_bgcolor='#F8F8FF'
)

# Adjust axes for the bar chart
fig['layout']['xaxis'].update(domain=[0.0, .06])
fig['layout']['yaxis'].update(domain=[0.22, 1], title="Market Cap (in Billions of USD)")

# Sankey positioning within combined plot
fig.update_traces(
    selector=dict(type='sankey'),
    domain=dict(x=[0.07, 1.00], y=[0.05, 0.95])
)

# Display figure
fig.show()
