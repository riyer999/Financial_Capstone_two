import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

# Sample data
data = {
    "Category": ["Fruit", "Fruit", "Fruit", "Vegetable", "Vegetable", "Vegetable"],
    "Item": ["Apple", "Banana", "Grapes", "Carrot", "Broccoli", "Spinach"],
    "Amount": [500, 300, 200, 150, 100, 80]
}
df = pd.DataFrame(data)

# Initialize the Dash app with suppress_callback_exceptions=True
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Main layout with dcc.Location to handle URL changes and a placeholder for dynamic content
app.layout = html.Div([
    dcc.Location(id='url', refresh=True),  # URL component for redirection
    html.Div(id='page-content'),           # Dynamic content based on the URL
])

# Main page layout with the treemap
main_page_layout = html.Div([
    html.H1("Treemap Example with Plotly and Dash"),
    dcc.Graph(
        id="treemap",
        figure=px.treemap(df, path=["Category", "Item"], values="Amount"),
        clickData=None  # Initialize with no click data
    ),
])

# Callback to update page layout based on URL
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    # Display the main page layout
    if pathname == '/' or pathname == '':
        return main_page_layout
    # Display a blank page for each item clicked, with a button to go back
    elif pathname.startswith('/item/'):
        item_name = pathname.split('/')[-1]
        return html.Div([
            html.H1(f"Details for {item_name.capitalize()}"),
            html.P("This is a blank page where you can add more information about this item."),
            html.Br(),
            # Button to return to the main page
            html.A(
                html.Button("Back to Treemap", id="back-button"),
                href="/"  # URL to navigate back to the root page
            )
        ])

# Callback to handle item clicks in the treemap and redirect to a new URL
@app.callback(
    Output('url', 'pathname'),
    Output('treemap', 'figure'),
    Input('treemap', 'clickData')
)
def update_treemap(click_data):
    # Check if an item was clicked
    if click_data:
        item_name = click_data['points'][0]['label']
        if item_name in df['Item'].values:
            # Item clicked, navigate to the item page
            return f'/item/{item_name}', px.treemap(df, path=["Category", "Item"], values="Amount")
        else:
            # Category clicked, zoom into that category
            category_name = click_data['points'][0]['label']
            filtered_df = df[df['Category'] == category_name]
            return '/',''  # No URL change, zoom in within the same page
    return '/', px.treemap(df, path=["Category", "Item"], values="Amount")


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
