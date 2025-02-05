import pandas as pd
import numpy as np

# Assuming 'equitybond_df' contains the data with 'Ticker' and 'Equity Bond'
# If not, load your data like this: equitybond_df = pd.read_csv('filtered_equity_bond_data.csv')
equitybond_df = pd.read_csv('filtered_equity_bond_data.csv')
# Define the treasury rate and its corresponding scale
treasury_rate = 4.0  # Treasury rate in percentage
treasury_rate_scale = 3  # This corresponds to a rating of 3 (for treasury rate)

# Define the minimum and maximum equity bond values (these can be calculated from your data)
min_equity_bond = equitybond_df['Equity Bond'].min()
max_equity_bond = equitybond_df['Equity Bond'].max()

# Normalize function to scale the Equity Bond values to a 1-5 scale
def scale_price(equity_bond_value, min_value, max_value, treasury_rate, treasury_rate_scale):
    # Adjust the scale based on the treasury rate
    scaled_value = ((equity_bond_value - min_value) / (max_value - min_value)) * 4 + 1  # Scale between 1-5
    # Adjust the value to align with the treasury rate
    if equity_bond_value >= treasury_rate:
        scaled_value = min(scaled_value, 5)  # Maximum rating for expensive companies
    elif equity_bond_value <= treasury_rate:
        scaled_value = max(scaled_value, 1)  # Minimum rating for cheaper companies
    return np.round(scaled_value, 2)

# Add a column with the scaled price
equitybond_df['Price Rating'] = equitybond_df['Equity Bond'].apply(
    lambda x: scale_price(x, min_equity_bond, max_equity_bond, treasury_rate, treasury_rate_scale)
)

# Generate the justification for the price rating
def price_justification(row):
    if row['Equity Bond'] > treasury_rate:
        return f"Expensive: Equity Bond value of {row['Equity Bond']}% is higher than the treasury rate of {treasury_rate}%."
    elif row['Equity Bond'] < treasury_rate:
        return f"Cheap: Equity Bond value of {row['Equity Bond']}% is lower than the treasury rate of {treasury_rate}%. "
    else:
        return f"Fair: Equity Bond value is equal to the treasury rate of {treasury_rate}%. "

equitybond_df['Justification'] = equitybond_df.apply(price_justification, axis=1)

# Display the updated DataFrame with Price Rating and Justification
print(equitybond_df[['Ticker', 'Equity Bond', 'Price Rating', 'Justification']])

# Optionally, save the result to a new CSV
equitybond_df.to_csv('equity_bond_price_ratings.csv', index=False)
