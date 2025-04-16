from edgar import set_identity, Company, get_filings
from edgar.financials import Financials

set_identity("Matthew Sun Matthew.Sun@uscga.edu")
stock = Company("MET")
filings = stock.get_filings(form = "10-K")

for i in range(0, 4):
    tenk = filings[i].obj()

    financials = tenk.financials
    balance_sheet_df = financials.get_balance_sheet().get_dataframe()
    print(balance_sheet_df)