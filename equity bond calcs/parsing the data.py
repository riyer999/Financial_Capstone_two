import pandas as pd
import re

# Load the data from the CSV file
file_path = '../equitybond.csv'
with open(file_path, 'r') as file:
    data = file.readlines()

# Initialize a list to hold the company ticker and its equity bond value
valid_data = []

# Regular expression pattern to extract ticker and equity bond percentage
pattern = re.compile(r"([A-Za-z]+): Equity Bond = (-?\d+\.\d+)")

# Process each line
for line in data:
    match = pattern.match(line)
    if match:
        ticker = match.group(1)
        equity_bond = float(match.group(2))
        # Add the data to the list if it's a valid entry
        valid_data.append([ticker, equity_bond])

# Create a DataFrame from the valid data
df = pd.DataFrame(valid_data, columns=["Ticker", "Equity Bond"])

# Store the filtered data to a new CSV file
df.to_csv('filtered_equity_bond_data.csv', index=False)

print("Filtered data has been saved to 'filtered_equity_bond_data.csv'.")
