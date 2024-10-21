import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL of the Wikipedia page containing S&P 500 companies
url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"

# Fetch the webpage
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table containing the S&P 500 companies
table = soup.find('table', {'class': 'wikitable'})

# Extract the data
tickers = []
companies = []
industries = []

# Iterate through the rows of the table
for row in table.find_all('tr')[1:]:  # Skip the header row
    cols = row.find_all('td')
    if len(cols) > 0:
        ticker = cols[0].text.strip()  # Ticker symbol
        company = cols[1].text.strip()  # Company name
        industry = cols[2].text.strip()  # Industry
        tickers.append(ticker)
        companies.append(company)
        industries.append(industry)

# Create a DataFrame for better handling
sp500_df = pd.DataFrame({
    'Ticker': tickers,
    'Company': companies,
    'Industry': industries
})

# Show the first few rows of the DataFrame
print(sp500_df.head())

# Save to CSV if needed
sp500_df.to_csv('sp500_companies_industries.csv', index=False)
