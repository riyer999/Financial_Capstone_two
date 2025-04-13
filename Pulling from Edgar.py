import pickle
import os
import pandas as pd
from edgar import set_identity, Company

# Function to safely convert values to float
def safe_float(value):
    try:
        # Attempt to convert value to float, and handle any conversion errors
        return float(value) if value else 0.0
    except ValueError:
        return 0.0  # Return 0.0 if value can't be converted to float

# Function to process each ticker and save its data as a .pkl file
def process_ticker(ticker, target_years, selected_concepts):
    # Create a dictionary to store concept values for each year
    variable_names = {}

    # Set identity and get filings
    set_identity("x x x.x@uscga.edu")
    stock = Company(ticker)
    filings = stock.get_filings(form="10-K")

    # Loop through filings and extract values for selected concepts
    for year in range(len(target_years)):  # Iterate through filings for multiple years
        tenk = filings[year].obj()
        financials = tenk.financials
        balance_sheet_df = financials.get_balance_sheet().get_dataframe()

        # Identify available year columns dynamically
        available_years = [col for col in balance_sheet_df.columns if col.isdigit()]

        # Extract values for each target year that exists in the DataFrame
        for target_year in target_years:
            if target_year in available_years:
                # Filter for the selected concepts in the target year
                filtered_df = balance_sheet_df.loc[
                    balance_sheet_df["concept"].isin(selected_concepts), ["concept", target_year]
                ]

                # Store values for each concept in the dictionary if found
                for concept in selected_concepts:
                    concept_value = filtered_df[filtered_df["concept"] == concept].set_index("concept").get(target_year)

                    # Safely convert each concept value to float before storing
                    if not concept_value.empty:
                        # Extract the part of the concept name after the last underscore
                        concept_name = concept.split("_")[-1]

                        # Store the value with the new concept name (after the last underscore)
                        variable_names[concept_name + f"_{target_year}"] = safe_float(concept_value.iloc[0])

    # Define the directory for saving files
    directory = "pkl_files"

    # Create the directory if it doesn't exist
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Create a filename based on the ticker
    filename = f"{ticker}_financials.pkl"

    # Define the full path to save the file in the "pkl files" directory
    file_path = os.path.join(directory, filename)

    # Save the dictionary as a .pkl file in the specified directory
    with open(file_path, "wb") as f:
        pickle.dump(variable_names, f)

    print(f"Saved {ticker}_financials.pkl")

# Main function to process all tickers in the CSV
def process_all_tickers(csv_file):
    # Read the CSV file containing the tickers
    df = pd.read_csv(csv_file)

    # Define the target years and selected concepts for extraction
    target_years = ["2021", "2022", "2023", "2024"]
    selected_concepts = [
        "us-gaap_Deposits",
        "us-gaap_LiabilityForClaimsAndClaimsAdjustmentExpensePropertyCasualtyLiability",
        "us-gaap_LiabilityForFuturePolicyBenefits",
        "us-gaap_PolicyholderContractDeposits",
        "us-gaap_UnearnedPremiums",
        "all_ClaimPaymentsOutstanding",
        "us-gaap_AccruedLiabilitiesAndOtherLiabilities"
    ]

    # Loop through each ticker in the DataFrame and process it
    for ticker in df['Ticker']:
        process_ticker(ticker, target_years, selected_concepts)

# Run the process on your CSV file
csv_file = "fake_csv.csv"  # Path to your CSV file with tickers
process_all_tickers(csv_file)
