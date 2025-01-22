import plotly.graph_objects as go

# Define the Sankey diagram data
nodes = {
    'label': ["Node 1", "Node 2", "Node 3", "Node 4"],
}

links = {
    'source': [0, 1, 0, 1],
    'target': [2, 2, 3, 3],
    'value': [8, 4, 2, 8],
}

# Define custom hover labels for nodes
custom_hover_labels = [
    "Lion",       # Node 1
    "Tiger",      # Node 2
    "Panda",      # Node 3
    "Gorilla"     # Node 4
]

# Create the Sankey diagram
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=nodes['label'],             # Labels for nodes
        customdata=custom_hover_labels,  # Add custom animal labels
        hovertemplate="Animal: %{customdata}<extra></extra>",  # Show custom animal names
    ),
    link=dict(
        source=links['source'],
        target=links['target'],
        value=links['value'],
    )
)])

# Show the figure
fig.show()
