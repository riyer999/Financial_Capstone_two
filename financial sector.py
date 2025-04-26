import pandas as pd

# Load the CSV file
file_path = 'sp500_companies_industries.csv'  # Replace with your actual file name
df = pd.read_csv(file_path)

# Filter for only Finance industry
finance_df = df[df['Industry'] == 'Financials']  # Change to 'Finance' if needed

# Output the result
print(finance_df)

# Optional: Save to a new CSV
finance_df.to_csv('finance_companies.csv', index=False)
