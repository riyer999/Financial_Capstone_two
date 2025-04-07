from edgar import set_identity, Company
import pandas as pd

set_identity("a a k.s@uscga.edu")

# Inspect available methods for get_filings
filings = Company.for_ticker("JPM").get_filings(form="10-K")
print(dir(filings))  # Print available methods and attributes
