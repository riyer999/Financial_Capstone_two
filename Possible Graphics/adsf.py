if total_revenue > 0:
    sankey_fig.add_annotation(dict(font=dict(color="steelblue", size=12), x=0.08, y=0.99, showarrow=False,
                                   text='<b>Revenue</b>'))
    sankey_fig.add_annotation(dict(font=dict(color="steelblue", size=12), x=0.08, y=0.96, showarrow=False,
                                   text=f'<b>${total_revenue:.1f}B</b>'))

# Gross Profit
if gross_profit_value > 0:
    sankey_fig.add_annotation(dict(font=dict(color="green", size=12), x=0.315, y=0.99, showarrow=False,
                                   text='<b>Gross Profit</b>'))
    sankey_fig.add_annotation(dict(font=dict(color="green", size=12), x=0.33, y=0.96, showarrow=False,
                                   text=f'<b>${gross_profit_value:.1f}B</b>'))

# Operating Profit
if operating_income > 0:
    sankey_fig.add_annotation(dict(font=dict(color="green", size=12), x=0.61, y=1.05, showarrow=False,
                                   text='<b>Operating Profit</b>'))
    sankey_fig.add_annotation(dict(font=dict(color="green", size=12), x=0.61, y=1.02, showarrow=False,
                                   text=f'<b>${operating_income:.1f}B</b>'))

# Net Profit
if net_income > 0:
    sankey_fig.add_annotation(dict(font=dict(color="green", size=12), x=0.95, y=1.05, showarrow=False,
                                   text='<b>Net Profit</b>'))
    sankey_fig.add_annotation(dict(font=dict(color="green", size=12), x=0.94, y=1, showarrow=False,
                                   text=f'<b>${net_income:.1f}B</b>'))

# Tax
if tax_provision > 0:
    sankey_fig.add_annotation(
        dict(font=dict(color="maroon", size=12), x=0.93, y=0.9, showarrow=False, text='<b>Tax</b>'))
    sankey_fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.935, y=0.85, showarrow=False,
                                   text=f'<b>${tax_provision:.1f}B</b>'))

# Other
if other > 0:
    sankey_fig.add_annotation(
        dict(font=dict(color="maroon", size=12), x=0.935, y=0.75, showarrow=False, text='<b>Other</b>'))
    sankey_fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.935, y=0.70, showarrow=False,
                                   text=f'<b>${other:.1f}B</b>'))

# SG&A
if sga > 0:
    sankey_fig.add_annotation(
        dict(font=dict(color="maroon", size=12), x=0.93, y=0.58, showarrow=False, text='<b>SG&A</b>'))
    sankey_fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.93, y=0.52, showarrow=False,
                                   text=f'<b>${sga:.1f}B</b>'))

# Other Operating Expenses
if other_operating_expenses > 0:
    sankey_fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.95, y=0.40, showarrow=False,
                                   text='<b>Other<br>Operating<br>Expenses</b>'))
    sankey_fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.935, y=0.26, showarrow=False,
                                   text=f'<b>${other_operating_expenses:.1f}B</b>'))

# Operating Expenses
if operating_expense > 0:
    sankey_fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.59, y=0.41, showarrow=False,
                                   text='<b>Operating<br>Expenses</b>'))
    sankey_fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.59, y=0.34, showarrow=False,
                                   text=f'<b>${operating_expense:.1f}B</b>'))

# Cost of Revenues
if cost_revenue > 0:
    sankey_fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.34, y=0.08, showarrow=False,
                                   text='<b>Cost of<br>Revenues</b>'))
    sankey_fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.34, y=0.05, showarrow=False,
                                   text=f'<b>${cost_revenue:.1f}B</b>'))