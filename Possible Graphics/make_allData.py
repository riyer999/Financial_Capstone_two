import yfinance as yf #imports the yfinanance library to fetch financial information
import pickle #import pickle to save and load python objects

#https://rfachrizal.medium.com/how-to-obtain-financial-statements-from-stocks-using-yfinance-87c432b803b8 #gives more of an explanation for how this works

#Import tickerList as a list: reads the ticker list from a text file
with open('0_tickerList.txt', 'r') as file: #don't really need this if you end up specifying which tickers to use
    tickerList = [line.strip() for line in file.readlines()]

#Master dictionary is called allData
allData = {} #initializing an empty dictionary to store all financial data for each company
tickerList = ['AAPL','KO', 'TSM', 'AMZN', 'PEP'] #the list of companies that you fetching financial information for
for ticker in tickerList:
    try:
        print(ticker) #print the ticker to track the progress of fetching the information
        #Temp dictionary stores the info below
        temp = {} #empty dictionary for each ticker to store its financial info
        ystock = yf.Ticker(ticker) #creating a yfinance ticker object
        temp['balance_sheet']=ystock.balance_sheet #fetching each respective financial statement and storing them in the temp dictionary
        temp['income_statement']=ystock.incomestmt
        temp['cashflow_statement']=ystock.cashflow
        temp['info']=ystock.info #this gets information like the market cap and other stuff
        temp['hist']=ystock.history(period='max') #fetches the historical stocck price for the last 5 years
        #Ticker, temp dict pair added to master dictionary
        allData[ticker] = temp
    except Exception as e: #error case
        print('Error')

#Save data to allData.pkl file
with open('allData.pkl', 'wb') as file:
    pickle.dump(allData, file) #dumps the allData dictionary into a pickle file


#THIS FILE GENERATES THE allData.pkl





