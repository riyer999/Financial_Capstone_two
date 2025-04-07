import pickle
from edgar import set_identity, Company
import pandas as pd
ticker = 'JPM'
set_identity("x x x.x@uscga.edu")
stock = Company(ticker)
filings = stock.get_filings(form="10-K")

# Define the target years for extraction
target_years = ["2021", "2022", "2023", "2024"]
selected_concepts = ["us-gaap_Deposits"]

# Dictionary to store deposit values for each year
variable_names = {}

# Function to safely convert values to float
def safe_float(value):
    try:
        # Attempt to convert value to float, and handle any conversion errors
        return float(value) if value else 0.0
    except ValueError:
        return 0.0  # Return 0.0 if value can't be converted to float

# Loop through filings and extract deposit values
for year in range(len(target_years)):  # Iterate through filings for multiple years
    tenk = filings[year].obj()
    financials = tenk.financials
    balance_sheet_df = financials.get_balance_sheet().get_dataframe()

    # Identify available year columns dynamically
    available_years = [col for col in balance_sheet_df.columns if col.isdigit()]

    # Extract deposits for each target year that exists in the DataFrame
    for target_year in target_years:
        if target_year in available_years:
            # Filter for the selected concept (us-gaap_Deposits) in the target year
            filtered_df = balance_sheet_df.loc[
                balance_sheet_df["concept"].isin(selected_concepts), ["concept", target_year]
            ]

            # Store deposit value in dictionary if found
            if not filtered_df.empty:
                deposit_value = filtered_df.set_index("concept")[target_year].to_dict().get("us-gaap_Deposits")
                # Safely convert the deposit value to float before storing
                variable_names[f"Deposits_{target_year}"] = safe_float(deposit_value)

# Print the final dictionary with deposit values from 2021-2024

filename = f"{ticker}_deposits.pkl"
# Save the dictionary as a .pkl file
with open("jpm_deposits.pkl", "wb") as f:
    pickle.dump(variable_names, f)

# To load the dictionary later
with open("jpm_deposits.pkl", "rb") as f:
    loaded_data = pickle.load(f)

print(variable_names)

# Check the types of values in the dictionary
#for key, value in variable_names.items():
 #   print(f"Key: {key}, Type of Value: {type(value)}")



