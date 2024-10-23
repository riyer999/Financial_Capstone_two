import plotly.graph_objects as go

# Define the data for the Sankey diagram
labels = ['Total Revenue', "Gross Profit", "Cost of Goods Sold","Selling, General, and Admin", "Operating Profit" ]

#labels = ['Revenue', 'Gross Profit', 'Gross Profit', 'Operating Profit', 'Interest','Net Profit', 'Tax', 'Sales & Marketing', 'General & Administrative']
# Indices for the links
source = [0, 1, 1, 2, 2, 2, 5, 5, 5]
target = [1, 2, 3, 4, 5, 6, 7, 8, 9]
# Values for the links
values = [11, 6.7, 4.3, 3.2, 3.4, .1, 3.1, .9, .2]  # Flow amounts between nodes

x_positions = [0.1, 0.3, 0.3, 0.5, 0.7]  # X coordinates of the nodes
y_positions = [0.5, 0.3, 0.6, 0.5, 0.5]  # Moved 'Gross Profit' down to 0.3

# Create the Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=100,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels,

    ),
    link=dict(
        source=source,  # Indices of the source nodes
        target=target,  # Indices of the target nodes
        value=values,   # Values for the flows
        color=['gray', 'green', 'red', 'red ', 'green','red', 'green', 'green', 'red'],
    )
)])

# Update layout
fig.update_layout(title_text="Basic Sankey Diagram", font_size=10)

# Show the figure
fig.show()
