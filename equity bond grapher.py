import pandas as pd
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# Read the filtered data from the CSV file into a DataFrame
equitybond_df = pd.read_csv('filtered_equity_bond_data.csv')

# Check the first few rows to inspect the data
print(equitybond_df.head())

# Drop any rows where the 'Equity Bond' value is NaN (if any remain)
equity_bonds = equitybond_df['Equity Bond'].dropna()

# Print the cleaned data (optional, for debugging)
print(equity_bonds)

# Plot the distribution of the Equity Bond values with 500 bins
plt.figure(figsize=(10, 6))
plt.hist(equity_bonds, bins=200, alpha=0.7, color='blue', edgecolor='black')
plt.xlabel("Equity Bond (%)")
plt.ylabel("Number of Companies")
plt.title("Distribution of Equity Bonds")

# Add a red vertical line at 4% and label it as "US Treasury Interest Rate"
plt.axvline(x=4, color='red', linestyle='--', linewidth=2)  # Vertical line at 4%


# Example: Add a specific company (e.g., 'ACME') with a given Equity Bond value
company_ticker = 'ACME'
company_equity_bond = 10  # Replace this with the actual value of the company
plt.scatter(company_equity_bond, 5, color='green', label=f'{company_ticker} Equity Bond', zorder=5)

# Annotate the point with the company name
plt.text(company_equity_bond + 0.5, 5, f'{company_ticker}', color='green', fontsize=12, verticalalignment='center')

plt.grid(True)
plt.show()
