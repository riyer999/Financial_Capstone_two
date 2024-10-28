import plotly.graph_objects as go

import plotly.express as px
import yfinance as yf

#initialize market cap bar
bar_fig = go.Figure()

#plot the market cap
categories = ['Market Cap']
values = [293.2]


bar_fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color='steelblue'
))

bar_fig.update_layout(
    title='Financial Summary',
    xaxis_title='Categories',
    yaxis_title='Amount (in Billions)',
    barmode = 'group',
    paper_bgcolor='#F8F8FF'
)

color_link = ['#000000', '#FFFF00', '#1CE6FF', '#FF34FF', '#FF4A46',
             '#008941', '#006FA6', '#A30059','#FFDBE5', '#7A4900', 
             '#0000A6', '#63FFAC', '#B79762', '#004D43', '#8FB0FF',
             '#997D87', '#5A0007', '#809693', '#FEFFE6', '#1B4400', 
             '#4FC601', '#3B5DFF', '#4A3B53', '#FF2F80', '#61615A',
             '#BA0900', '#6B7900', '#00C2A0', '#FFAA92', '#FF90C9',
             '#B903AA', '#D16100', '#DDEFFF', '#000035', '#7B4F4B',                
             '#A1C299', '#300018', '#0AA6D8', '#013349', '#00846F',
             '#372101', '#FFB500', '#C2FFED', '#A079BF', '#CC0744',
             '#C0B9B2', '#C2FF99', '#001E09', '#00489C', '#6F0062', 
             '#0CBD66', '#EEC3FF', '#456D75', '#B77B68', '#7A87A1',
             '#788D66', '#885578', '#FAD09F', '#FF8A9A', '#D157A0',
             '#BEC459', '#456648', '#0086ED', '#886F4C', '#34362D', 
             '#B4A8BD', '#00A6AA', '#452C2C', '#636375', '#A3C8C9', 
             '#FF913F', '#938A81', '#575329', '#00FECF', '#B05B6F',
             '#8CD0FF', '#3B9700', '#04F757', '#C8A1A1', '#1E6E00',
             '#7900D7', '#A77500', '#6367A9', '#A05837', '#6B002C',
             '#772600', '#D790FF', '#9B9700', '#549E79', '#FFF69F', 
             '#201625', '#72418F', '#BC23FF', '#99ADC0', '#3A2465',
             '#922329', '#5B4534', '#FDE8DC', '#404E55', '#0089A3',
             '#CB7E98', '#A4E804', '#324E72', '#6A3A4C'
             ]

label = ['Revenue',
         'Gross Profit',
         'Cost of Revenues',
         'Operating Profit',
         'Operating Expenses',
         'TAC',
         'Others',
         'Net Profit',
         'Tax',
         'Other',
         'R&D',
         'S&M',
         'G&A'
        ]


color_for_nodes =['steelblue', 'green', 'red', 'green','red', 'red', 'red','green', 'red', 'red',
                  'red', 'red','red']

color_for_links =['lightgreen', 'PaleVioletRed', 'lightgreen', 'PaleVioletRed', 'PaleVioletRed', 'PaleVioletRed', 'lightgreen', 
                  'PaleVioletRed', 'PaleVioletRed', 'PaleVioletRed', 'PaleVioletRed', 'PaleVioletRed']

# Data 
source = [0, 0, 1, 1, 2, 2, 3, 3, 3, 4, 4, 4]
target = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
value = [37.9, 31.2, 17.1, 20.8, 11.8, 19.3, 13.9, 2.3, 0.9, 10.3, 6.9, 3.6 ]

link = dict(source=source, target=target, value=value, color=color_link)
node = dict(label = label, pad=35, thickness=20)
data = go.Sankey(link=link, node=node)

x = [   0.1, 0.35, 0.35,  0.6, 0.6, 0.6,
      0.6, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85]
y = [  0.40, 0.25, 0.70, 0.1, 0.40, 
     0.70, 0.90, 0.0, 0.15, 0.30, 0.45, 0.60, 0.75]
x = [.001 if v==0 else .999 if v==1 else v for v in x]
y = [.001 if v==0 else .999 if v==1 else v for v in y]


sankey_fig = go.Figure(data=[go.Sankey(
    
    textfont=dict(color="black", size=10),
    node = dict(
        pad = 35,
        line = dict(color = "white", width = 1),
        label = label,
        x=x,
        y=y
    ),
    link = dict(
        source = source,
        target = target,
        value = value
        ))])


sankey_fig.update_layout(
    hovermode='x',
    title="<span style='font-size:36px;color:steelblue;'><b>KO FY23 Income Statement</b></span>",
    font=dict(size=10, color='white'),
    paper_bgcolor='#F8F8FF'
)

sankey_fig.update_traces(node_color = color_for_nodes,
                  link_color = color_for_links)



#x = [   0.1, 0.35, 0.35,  0.6, 0.6, 0.6,
#      0.6, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85]
#y = [  0.40, 0.25, 0.70, 0.1, 0.40, 
#     0.70, 0.90, 0.0, 0.15, 0.30, 0.45, 0.60, 0.75]
# Revenue
sankey_fig.add_annotation(dict(font=dict(color="steelblue",size=12), x=0.08, y=0.99, showarrow=False, text='<b>Revenue</b>'))
sankey_fig.add_annotation(dict(font=dict(color="steelblue",size=12), x=0.08, y=0.96, showarrow=False, text='<b>$69.1B</b>'))

# Gross Profit
sankey_fig.add_annotation(dict(font=dict(color="green",size=12), x=0.315, y=0.99, showarrow=False, text='<b>Gross Profit</b>'))
sankey_fig.add_annotation(dict(font=dict(color="green",size=12), x=0.33, y=0.96, showarrow=False, text='<b>$37.1B</b>'))


# Operating Profit
sankey_fig.add_annotation(dict(font=dict(color="green",size=12), x=0.61, y=1.05, showarrow=False, text='<b>Operating Profit</b>'))
sankey_fig.add_annotation(dict(font=dict(color="green",size=12), x=0.61, y=1.02, showarrow=False, text='<b>$16.1B</b>'))


# Net Profit
sankey_fig.add_annotation(dict(font=dict(color="green",size=12), x=0.95, y=1.05, showarrow=False, text='<b>Net Profit</b>'))
sankey_fig.add_annotation(dict(font=dict(color="green",size=12), x=0.94, y=1, showarrow=False, text='<b>$13.9B</b>'))

# Operating Profit Tax
sankey_fig.add_annotation(dict(font=dict(color="maroon",size=12), x=0.93, y=0.9, showarrow=False, text='<b>Tax</b>'))
sankey_fig.add_annotation(dict(font=dict(color="maroon",size=12), x=0.935, y=0.85, showarrow=False, text='<b>$2.3B</b>'))

# Operating Profit Other
sankey_fig.add_annotation(dict(font=dict(color="maroon",size=12), x=0.935, y=0.75, showarrow=False, text='<b>Other</b>'))
sankey_fig.add_annotation(dict(font=dict(color="maroon",size=12), x=0.935, y=0.70, showarrow=False, text='<b>$0.9B</b>'))

# Operating Profit R&D
sankey_fig.add_annotation(dict(font=dict(color="maroon",size=12), x=0.93, y=0.58, showarrow=False, text='<b>R&D</b>'))
sankey_fig.add_annotation(dict(font=dict(color="maroon",size=12), x=0.94, y=0.53, showarrow=False, text='<b>$10.3B</b>'))

# Operating Profit S&M
sankey_fig.add_annotation(dict(font=dict(color="maroon",size=12), x=0.93, y=0.43, showarrow=False, text='<b>S&M</b>'))
sankey_fig.add_annotation(dict(font=dict(color="maroon",size=12), x=0.935, y=0.38, showarrow=False, text='<b>$6.9B</b>'))

# Operating Profit G&A
sankey_fig.add_annotation(dict(font=dict(color="maroon",size=12), x=0.93, y=0.25, showarrow=False, text='<b>G&A</b>'))
sankey_fig.add_annotation(dict(font=dict(color="maroon",size=12), x=0.935, y=0.20, showarrow=False, text='<b>$3.6B</b>'))

# Operating Expenses
sankey_fig.add_annotation(dict(font=dict(color="maroon",size=12), x=0.59, y=0.47, showarrow=False, text='<b>Operating<br>expenses</b>'))
sankey_fig.add_annotation(dict(font=dict(color="maroon",size=12), x=0.59, y=0.41, showarrow=False, text='<b>$20.8B</b>'))

# Cost of Revenues
sankey_fig.add_annotation(dict(font=dict(color="maroon",size=12), x=0.34, y=0.08, showarrow=False, text='<b>Cost of<br>Revenues</b>'))
sankey_fig.add_annotation(dict(font=dict(color="maroon",size=12), x=0.34, y=0.05, showarrow=False, text='<b>$31.2B</b>'))

# TAC
sankey_fig.add_annotation(dict(font=dict(color="maroon",size=12), x=0.65, y=0.30, showarrow=False, text='<b>TAC</b>'))
sankey_fig.add_annotation(dict(font=dict(color="maroon",size=12), x=0.68, y=0.25, showarrow=False, text='<b>$11.8B</b>'))

# Cost of Revenues - Others
sankey_fig.add_annotation(dict(font=dict(color="maroon",size=12), x=0.68, y=0.10, showarrow=False, text='<b>Others</b>'))
sankey_fig.add_annotation(dict(font=dict(color="maroon",size=12), x=0.68, y=0.05, showarrow=False, text='<b>$19.3B</b>'))

fig = make_subplots(
    rows=1, cols=2,
    column_widths=[0.05, 0.95],
    #subplot_titles = ("Market Cap"),
    specs = [[{"type": "bar"}, {"type": "sankey"}]]
)

fig.update_xaxes(showticklabels=False, tickvals=[], row=1, col=1)

for trace in bar_fig.data:
    fig.add_trace(trace, row=1, col=1)

for trace in sankey_fig.data:
    fig.add_trace(trace, row=1, col=2)

fig.update_layout(
    title_text="Market Cap and Financial Summary",
    paper_bgcolor='#F8F8FF'
)

fig.update_yaxes(
    scaleanchor=None,
    row=1, col=2
)

#positioning for Sankey graph
fig.update_traces(
    selector=dict(type='sankey'),
    domain=dict(x=[0.00, 1.00], y=[0.01,0.5])
)
fig['layout']['xaxis'].update(domain=[0.0, .06])  # X domain for the bar chart ###
fig['layout']['yaxis'].update(domain=[0.22, 1])    # Y domain for the bar chart ###

fig.show()