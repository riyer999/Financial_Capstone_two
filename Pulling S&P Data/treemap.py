import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import squarify

# Read the S&P 500 data from the CSV file
sp500_df = pd.read_csv('sp500_companies_industries.csv')


# Function to get market capitalization
def get_market_cap(ticker_symbol):
    stock = yf.Ticker(ticker_symbol)
    market_cap = stock.info.get('marketCap', None)
    return market_cap


# Initialize lists for industry aggregation
industry_data = {}

# Iterate over the DataFrame to get market cap
for index, row in sp500_df.iterrows():
    ticker = row['Ticker']
    industry = row['Industry']
    market_cap = get_market_cap(ticker)

    if market_cap is not None:
        if industry not in industry_data:
            industry_data[industry] = 0
        industry_data[industry] += market_cap

# Prepare data for plotting
labels = list(industry_data.keys())
sizes = list(industry_data.values())

# Ensure there's data to visualize
if not sizes:
    print("No valid market cap data found.")
else:
    # Create a color map for industries
    colors = plt.cm.Set3.colors
    industry_colors = {industry: colors[i % len(colors)] for i, industry in enumerate(labels)}

    block_colors = [industry_colors[industry] for industry in labels]

    # Plot the treemap
    plt.figure(figsize=(12, 8))
    squarify.plot(sizes=sizes, label=labels, color=block_colors, alpha=0.7)

    plt.title('Market Capitalization Treemap for S&P 500 Industries')
    plt.axis('off')

    # Create a legend for industries
    plt.legend(handles=[plt.Rectangle((0, 0), 1, 1, color=industry_colors[industry]) for industry in labels],
               labels=labels, loc='upper left')

    plt.show()
