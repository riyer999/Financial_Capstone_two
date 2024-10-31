import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Create a subplot with 1 row and 2 columns
# Use specs to define the first subplot as a bar plot and the second as a Sankey plot
fig = make_subplots(rows=1, cols=2, specs=[[{"type": "bar"}, {"type": "sankey"}]])

# Add a bar trace to the first subplot
fig.add_trace(go.Bar(x=['Category 1', 'Category 2', 'Category 3'], y=[4, 5, 6], name="Bar Chart"), row=1, col=1)

# Define the data for the Sankey diagram
sankey_data = {
    'node': {
        'pad': 15,
        'thickness': 20,
        'line': {'color': 'black', 'width': 0.5},
        'label': ['A', 'B', 'C', 'D'],
    },
    'link': {
        'source': [0, 1, 0, 2, 3],  # Indices of the source nodes
        'target': [2, 2, 3, 3, 1],  # Indices of the target nodes
        'value': [8, 4, 2, 8, 4],   # Values corresponding to the links
    },
}

# Add the Sankey diagram to the second subplot
fig.add_trace(go.Sankey(**sankey_data), row=1, col=2)

# Add annotations to the Sankey plot
annotations = [
    dict(
        x=0,  # X position for node A
        y=0.2,  # Y position adjusted for visibility
        text="Source A",
        showarrow=True,
        arrowhead=2,
        ax=50,  # Arrow tail X coordinate
        ay=0    # Arrow tail Y coordinate
    ),
    dict(
        x=0,  # X position for node B
        y=0.4,  # Y position adjusted for visibility
        text="Source B",
        showarrow=True,
        arrowhead=2,
        ax=50,
        ay=0
    ),
    dict(
        x=2,  # X position for node C
        y=0.4,  # Y position adjusted for visibility
        text="Target C",
        showarrow=True,
        arrowhead=2,
        ax=-50,
        ay=0
    ),
    dict(
        x=3,  # X position for node D
        y=0.2,  # Y position adjusted for visibility
        text="Target D",
        showarrow=True,
        arrowhead=2,
        ax=-50,
        ay=0
    ),
]

# Add annotations to the figure
for annotation in annotations:
    fig.add_annotation(annotation)

# Update layout for better visualization
fig.update_layout(title_text='Bar Chart and Sankey Diagram with Annotations')

fig.show()
