import plotly.graph_objects as go
from plotly.subplots import make_subplots

def normalize_company_name(company_name, dataframe, column="Company"):
    # Normalize company name for matching
    dataframe['Normalized_Company'] = dataframe[column].str.strip().str.lower()
    return company_name.strip().lower()

def prepare_financial_metrics(financial_metrics, selected_year):
    # Extract and scale financial metrics for a specific year
    metric_keys = [
        "Total_Revenue", "Gross_Profit", "Cost_Of_Revenue",
        "Operating_Income", "Operating_Expense", "Tax_Provision",
        "Selling_General_And_Administration", "Other_Income_Expense",
        "Net_Income", "General_And_Administrative_Expense",
        "Other_Operating_Expenses"
    ]
    return {metric: financial_metrics[f"{metric}_{selected_year}"] / 1e9 for metric in metric_keys}

def create_bar_chart(ticker):
    # Create a bar chart for market cap
    categories = ['Market Cap']
    values = [get_market_cap(ticker)]
    bar_fig = go.Figure()
    bar_fig.add_trace(go.Bar(x=categories, y=values, marker_color='steelblue'))
    bar_fig.update_layout(
        title='Financial Summary',
        xaxis_title='Categories',
        yaxis_title='Amount (in Billions)',
        barmode='group',
        paper_bgcolor='#F8F8FF'
    )
    return bar_fig

def create_sankey_chart(financial_values):
    # Create a Sankey diagram using financial metrics
    labels = [
        'Revenue', 'Gross Profit', 'Cost of Revenues',
        'Operating Profit', 'Operating Expenses', 'Net Profit',
        'Tax', 'Other', 'SG&A', 'Other Expenses'
    ]
    colors_nodes = ['steelblue', 'green', 'red', 'green', 'red', 'green', 'red', 'red', 'red', 'red']
    colors_links = ['lightgreen', 'PaleVioletRed', 'lightgreen', 'PaleVioletRed', 
                    'lightgreen', 'PaleVioletRed', 'PaleVioletRed', 'PaleVioletRed', 'PaleVioletRed']
    
    source = [0, 0, 1, 1, 3, 3, 3, 4, 4]
    target = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    value = [
        financial_values["Gross_Profit"], financial_values["Cost_Of_Revenue"],
        financial_values["Operating_Income"], financial_values["Operating_Expense"],
        financial_values["Net_Income"], financial_values["Tax_Provision"],
        financial_values["Other_Income_Expense"], financial_values["Selling_General_And_Administration"],
        financial_values["Other_Operating_Expenses"]
    ]
    
    sankey_fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=35,
            thickness=20,
            label=labels,
            color=colors_nodes
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color=colors_links
        )
    )])
    sankey_fig.update_layout(
        title="<b>Income Statement</b>",
        font=dict(size=10),
        paper_bgcolor='#F8F8FF'
    )
    return sankey_fig

def combine_charts(bar_fig, sankey_fig):
    # Combine bar chart and Sankey diagram into a single subplot
    fig = make_subplots(
        rows=1, cols=2, column_widths=[0.05, 0.95],
        specs=[[{"type": "bar"}, {"type": "sankey"}]]
    )
    for trace in bar_fig.data:
        fig.add_trace(trace, row=1, col=1)
    for trace in sankey_fig.data:
        fig.add_trace(trace, row=1, col=2)
    
    fig.update_layout(
        title_text="Market Cap and Income Statement",
        paper_bgcolor='#F8F8FF'
    )
    fig.update_traces(
        selector=dict(type='sankey'),
        domain=dict(x=[0.00, 1.00], y=[0.01, 0.5])
    )
    fig['layout']['xaxis'].update(domain=[0.0, .06])  # Adjust bar chart X domain
    fig['layout']['yaxis'].update(domain=[0.22, 1])  # Adjust bar chart Y domain
    
    return fig

def generate_graph(company_name, selected_year):
    if not company_name or not selected_year:
        return {}, {'display': 'none'}

    # Normalize company name
    company_name_normalized = normalize_company_name(company_name, treemap_df)
    
    # Get the ticker
    matched_tickers = treemap_df[treemap_df['Normalized_Company'] == company_name_normalized]['Ticker']
    if not matched_tickers.empty:
        ticker = matched_tickers.values[0]
        financial_metrics = load_data(ticker, years=[selected_year])
        if financial_metrics:
            financial_values = prepare_financial_metrics(financial_metrics, selected_year)
            bar_fig = create_bar_chart(ticker)
            sankey_fig = create_sankey_chart(financial_values)
            combined_fig = combine_charts(bar_fig, sankey_fig)
            return combined_fig, {'display': 'block'}
    return {}, {'display': 'none'}

