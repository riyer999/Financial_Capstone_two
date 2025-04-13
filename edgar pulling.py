import pickle
from edgar import set_identity, Company
import pandas as pd

ticker = 'JPM'
set_identity("x x x.x@uscga.edu")
stock = Company(ticker)
filings = stock.get_filings(form="10-K")

# Define target years and concepts
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

variable_names = {}


def safe_float(value):
    try:
        return float(value) if value else 0.0
    except ValueError:
        return 0.0


# Loop through filings
for i in range(len(target_years)):
    try:
        tenk = filings[i].obj()
        financials = tenk.financials
        balance_sheet_df = financials.get_balance_sheet().get_dataframe()

        available_years = [col for col in balance_sheet_df.columns if any(y in col for y in target_years)]

        for concept in selected_concepts:
            if concept in balance_sheet_df.index:
                for col in available_years:
                    for year in target_years:
                        if year in col:
                            value = balance_sheet_df.at[concept, col]
                            value = safe_float(value)
                            key_name = f"{concept}_{year}"
                            if key_name not in variable_names:
                                variable_names[key_name] = value
    except Exception as e:
        print(f"Error processing filing {i}: {e}")

# Save to pickle
filename = f"{ticker}_deposits.pkl"
with open(filename, "wb") as f:
    pickle.dump(variable_names, f)

print("Saved:", variable_names)
