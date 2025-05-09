import yfinance as yf
import requests
from yahooquery import Ticker
import time


session = requests.Session()
session.headers.update({'User-Agent': 'Mozilla/5.0'})

ystock = yf.Ticker("KO", session=session)
stock_info = ystock.info
try:
    income_statement = ystock.financials
    print(income_statement)
    balance_sheet = ystock.balance_sheet
    print(balance_sheet)
    cashflow_statement = ystock.cashflow  # This fetches the cash flow statement

    print(cashflow_statement)
    # Fetch the stock's information (including shares outstanding)


    outstanding_shares = stock_info.get('sharesOutstanding')

    current_price = stock_info.get('currentPrice')

    market_cap = stock_info.get('marketCap', None)
    ticker = "KO"
    stock = Ticker(ticker)
    ticker = "KO"
    summary_data = stock.get_summary_profile()

    # Extract the longBusinessSummary
    summary = summary_data.get(ticker, {}).get('longBusinessSummary', 'Summary not available.')
    print(summary)
except Exception as e:
    print("Error:", e)

