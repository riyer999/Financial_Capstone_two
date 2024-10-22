import plotly.graph_objects as go

import yfinance as yf
################################################
import pickle

ticker = 'KO'
year = '2023'

def load_data(ticker, year):  # Loads the financial data.
    with open('allData.pkl', 'rb') as file:  # Dictionary with the financial data information
        allData = pickle.load(file)

    income_statement = allData[ticker]['income_statement']

    # List of keys to extract from the income statement
    keys = [
      #  'Tax Effect Of Unusual Items',
      #  'Tax Rate For Calcs',
       # 'Normalized EBITDA',
        'Total Unusual Items',
        'Total Unusual Items Excluding Goodwill',
      #  'Reconciled Depreciation',
        #'Reconciled Cost Of Revenue',
       # 'EBITDA',
       # 'EBIT',
        'Net Interest Income',
        'Interest Expense',
        'Interest Income',
        'Normalized Income',
     #   'Total Expenses',
        'Total Operating Income As Reported',
     #   'Diluted Average Shares',
        'Basic Average Shares',
     #   'Diluted EPS',
    #    'Basic EPS',
        #'Diluted NI Availto Com Stockholders',
        'Net Income Common Stockholders',
        'Net Income',
        'Minority Interests',
        'Net Income Including Noncontrolling Interests',
        'Net Income Continuous Operations',
        'Tax Provision',
        'Pretax Income',
        'Other Income Expense',
       # 'Other Non Operating Income Expenses',
        #'Special Income Charges',
       # 'Write Off',
        'Impairment Of Capital Assets',

        #'Earnings From Equity Interest',
        #'Gain On Sale Of Security',
        'Net Non Operating Interest Income Expense',
        'Interest Expense Non Operating',
        #'Interest Income Non Operating',
        'Operating Income',
        'Operating Expense',
        'Other Operating Expenses',
      #  'Depreciation Amortization Depletion Income Statement',
       # 'Depreciation And Amortization In Income Statement',
        #'Amortization',
        #'Amortization Of Intangibles Income Statement',
        'Selling General And Administration',
        'General And Administrative Expense',
      #  'Selling And Marketing Expense',
        #'General And Administrative Expense',
        #'Other Gand A',
        #'Salaries And Wages',
        'Gross Profit',
        'Cost Of Revenue',
        'Total Revenue',
        'Operating Revenue'
    ]

    # Create a dictionary to hold variable names and their corresponding values
    variable_names = {key.replace(" ", "_"): income_statement.loc[key, year].item() for key in keys}

    return variable_names  # Return the dictionary with variable names and values

# Load the financial data
financial_metrics = load_data(ticker, year)
total_revenue = financial_metrics['Total_Revenue']/1000000000
gross_profit_value = financial_metrics['Gross_Profit']/1000000000
cost_revenue = financial_metrics['Cost_Of_Revenue']/1000000000
operating_income = financial_metrics['Operating_Income']/1000000000
operating_expense = financial_metrics['Operating_Expense']/1000000000
tax_provision = financial_metrics['Tax_Provision']/1000000000
sga = financial_metrics['Selling_General_And_Administration']/1000000000
other = financial_metrics['Other_Income_Expense']/1000000000
net_income = financial_metrics['Net_Income']/1000000000
ga = financial_metrics['General_And_Administrative_Expense']/1000000000
other_operating_expenses= financial_metrics['Other_Operating_Expenses']/1000000000



###################################################
color_link = ['#000000', '#FFFF00', '#1CE6FF', '#FF34FF', '#FF4A46',
              '#008941', '#006FA6', '#A30059', '#FFDBE5', '#7A4900',
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

label = ['Revenue',  # this one is fine
         'Gross Profit',  # this one is also fine
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

color_for_nodes = ['steelblue', 'green', 'red', 'green', 'red', 'green', 'red', 'red',
                   'red', 'red', 'red']

color_for_links = ['lightgreen', 'PaleVioletRed', 'lightgreen', 'PaleVioletRed', 
                   'lightgreen',
                   'PaleVioletRed', 'PaleVioletRed', 'PaleVioletRed', 'PaleVioletRed', 'PaleVioletRed']

# Data
source = [0, 0, 1, 1, 3, 3, 3, 4, 4, 4]
target = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#gross profit, cost of revenues,
value = [gross_profit_value, cost_revenue, operating_income, operating_expense, net_income, tax_provision, other, sga, other_operating_expenses]

link = dict(source=source, target=target, value=value, color=color_link)
node = dict(label=label, pad=35, thickness=20)
data = go.Sankey(link=link, node=node)

x = [0.1, 0.35, 0.35, 0.6, 
     0.6, 0.85, 0.85, 0.85, 0.85, 0.85]
y = [0.40, 0.25, 0.70, 0.1,
      0.45, 0.0, 0.15, 0.30, 0.45, 0.60]
x = [.001 if v == 0 else .999 if v == 1 else v for v in x]
y = [.001 if v == 0 else .999 if v == 1 else v for v in y]

fig = go.Figure(data=[go.Sankey(

    textfont=dict(color="rgba(0,0,0,0)", size=1),
    node=dict(
        pad=35,
        line=dict(color="white", width=1),
        label=label,
        x=x,
        y=y
    ),
    link=dict(
        source=source,
        target=target,
        value=value
    ))])

fig.update_layout(
    hovermode='x',
    title="<span style='font-size:36px;color:steelblue;'><b>KO FY23 Income Statement</b></span>",
    font=dict(size=10, color='white'),
    paper_bgcolor='#F8F8FF'
)

fig.update_traces(node_color=color_for_nodes,
                  link_color=color_for_links)

# x = [   0.1, 0.35, 0.35,  0.6, 0.6, 0.6,
#      0.6, 0.85, 0.85, 0.85, 0.85, 0.85, 0.85]
# y = [  0.40, 0.25, 0.70, 0.1, 0.40,
#     0.70, 0.90, 0.0, 0.15, 0.30, 0.45, 0.60, 0.75]
# Revenue
fig.add_annotation(dict(font=dict(color="steelblue", size=12), x=0.08, y=0.99, showarrow=False, text='<b>Revenue</b>'))
fig.add_annotation(dict(font=dict(color="steelblue", size=12), x=0.08, y=0.96, showarrow=False, text='<b>$69.1B</b>'))

# Gross Profit
fig.add_annotation(
    dict(font=dict(color="green", size=12), x=0.315, y=0.99, showarrow=False, text='<b>Gross Profit</b>'))
fig.add_annotation(dict(font=dict(color="green", size=12), x=0.33, y=0.96, showarrow=False, text=f'<b>${gross_profit_value:.1f}B</b>'))

# Operating Profit
fig.add_annotation(
    dict(font=dict(color="green", size=12), x=0.61, y=1.05, showarrow=False, text='<b>Operating Profit</b>'))
fig.add_annotation(dict(font=dict(color="green", size=12), x=0.61, y=1.02, showarrow=False, text='<b>$16.1B</b>'))

# Net Profit
fig.add_annotation(dict(font=dict(color="green", size=12), x=0.95, y=1.05, showarrow=False, text='<b>Net Profit</b>'))
fig.add_annotation(dict(font=dict(color="green", size=12), x=0.94, y=1, showarrow=False, text='<b>$13.9B</b>'))

# Operating Profit Tax
fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.93, y=0.9, showarrow=False, text='<b>Tax</b>'))
fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.935, y=0.85, showarrow=False, text='<b>$2.3B</b>'))

# Operating Profit Other
fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.935, y=0.75, showarrow=False, text='<b>Other</b>'))
fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.935, y=0.70, showarrow=False, text='<b>$0.9B</b>'))

# Operating Profit R&D
fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.93, y=0.58, showarrow=False, text='<b>R&D</b>'))
fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.94, y=0.53, showarrow=False, text='<b>$10.3B</b>'))

# Operating Profit S&M
fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.93, y=0.43, showarrow=False, text='<b>S&M</b>'))
fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.935, y=0.38, showarrow=False, text='<b>$6.9B</b>'))

# Operating Profit G&A
fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.93, y=0.25, showarrow=False, text='<b>G&A</b>'))
fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.935, y=0.20, showarrow=False, text='<b>$3.6B</b>'))

# Operating Expenses
fig.add_annotation(
    dict(font=dict(color="maroon", size=12), x=0.59, y=0.47, showarrow=False, text='<b>Operating<br>expenses</b>'))
fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.59, y=0.41, showarrow=False, text='<b>$20.8B</b>'))

# Cost of Revenues
fig.add_annotation(
    dict(font=dict(color="maroon", size=12), x=0.34, y=0.08, showarrow=False, text='<b>Cost of<br>Revenues</b>'))
fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.34, y=0.05, showarrow=False, text='<b>$31.2B</b>'))

# Cost of Revenues - Others
fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.68, y=0.10, showarrow=False, text='<b>Others</b>'))
fig.add_annotation(dict(font=dict(color="maroon", size=12), x=0.68, y=0.05, showarrow=False, text='<b>$19.3B</b>'))

fig.show()