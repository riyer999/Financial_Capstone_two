[33mcommit b2e0d2bd92dc7d5aa4181e243a7b98662478ebb5[m[33m ([m[1;36mHEAD[m[33m -> [m[1;32mmaster[m[33m, [m[1;31morigin/master[m[33m, [m[1;31morigin/HEAD[m[33m)[m
Merge: b1b4d5f 8963262
Author: Gillian Cascio <gillian.h.cascio@uscga.edu>
Date:   Mon Apr 7 15:18:47 2025 -0400

    pushing to merge

[1mdiff --cc app.py[m
[1mindex 88d3e1a,5d01d12..8fc43d0[m
[1m--- a/app.py[m
[1m+++ b/app.py[m
[36m@@@ -638,15 -647,43 +647,20 @@@[m [mdef generate_equity_bond(company, selec[m
  [m
      return fig  # Returns only the figure (Dash-friendly)[m
  [m
[32m+ # Function to safely convert values to float[m
[32m+ def safe_float(value):[m
[32m+     try:[m
[32m+         return float(value) if value else 0.0[m
[32m+     except ValueError:[m
[32m+         return 0.0  # Return 0.0 if value can't be converted to float[m
  [m
[31m- [m
[31m- def load_data(ticker, years=['2021', '2022', '2023', '2024']):[m
[31m-     # Fetch the data dynamically using yfinance[m
[32m+ # Main function to process the data[m
[32m+ def load_data(ticker, years=["2021", "2022", "2023", "2024"]):[m
      ystock = yf.Ticker(ticker)[m
[31m-     [m
[31m -    ##[m
[31m -    filename = f"{ticker}_deposits.pkl"[m
[32m+ [m
[31m -    # Dictionary to store the extracted values[m
[31m -    variable_names = {}[m
[31m -[m
[31m -    try:[m
[31m -        # Open and load the pickle file[m
[31m -        with open(filename, "rb") as f:[m
[31m -            data = pickle.load(f)  # Load the dictionary from the file[m
[31m -[m
[31m -        # Extract the required years from the loaded data[m
[31m -        for year in years:[m
[31m -            key = f"Deposits_{year}"[m
[31m -            if key in data:[m
[31m -                variable_names[key] = data[key][m
[31m -[m
[31m -    except FileNotFoundError:[m
[31m -        print(f"Warning: {filename} not found. Skipping...")[m
[31m -    except Exception as e:[m
[31m -        print(f"Error loading {filename}: {e}")[m
[31m -[m
[31m -[m
[31m -    print(variable_names)[m
      # Fetch the financial data[m
      income_statement = ystock.incomestmt[m
[31m -[m
[32m +    print(income_statement)[m
      balance_sheet = ystock.balance_sheet[m
      pd.set_option('display.max_rows', None)[m
      pd.set_option('display.max_columns', None)[m
