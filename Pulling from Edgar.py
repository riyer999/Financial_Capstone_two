import pickle
import os
import pandas as pd
from edgar import set_identity, Company

def safe_float(value):
    try:
        return float(value) if value else 0.0
    except ValueError:
        return 0.0

def process_ticker(ticker, target_years, selected_concepts):
    variable_names = {}

    set_identity("x x x.x@uscga.edu")
    try:
        stock = Company(ticker)
        filings = stock.get_filings(form="10-K")
    except Exception as e:
        print(f"Failed to fetch data for {ticker}: {e}")
        return

    for year in range(len(target_years)):
        try:
            tenk = filings[year].obj()
            financials = tenk.financials
            balance_sheet_df = financials.get_balance_sheet().get_dataframe()
        except Exception as e:
            print(f"Skipping {ticker} year {target_years[year]}: {e}")
            continue

        available_years = [col for col in balance_sheet_df.columns if col.isdigit()]

        for target_year in target_years:
            if target_year in available_years:
                filtered_df = balance_sheet_df.loc[
                    balance_sheet_df["concept"].isin(selected_concepts), ["concept", target_year]
                ]

                for concept in selected_concepts:
                    concept_value = filtered_df[filtered_df["concept"] == concept].set_index("concept").get(target_year)

                    if not concept_value.empty:
                        concept_name = concept.split("_")[-1]
                        variable_names[concept_name + f"_{target_year}"] = safe_float(concept_value.iloc[0])

    if variable_names:
        directory = "pkl_files"
        if not os.path.exists(directory):
            os.makedirs(directory)

        filename = f"{ticker}_financials.pkl"
        file_path = os.path.join(directory, filename)

        with open(file_path, "wb") as f:
            pickle.dump(variable_names, f)

        print(f"Saved {filename}")
    else:
        print(f"No data found for {ticker}. Skipping file save.")

def process_all_tickers(csv_file):
    df = pd.read_csv(csv_file)

    target_years = ["2021", "2022", "2023", "2024"]
    selected_concepts = [
        "us-gaap_Deposits",
    ]

    for ticker in df['Ticker']:
        process_ticker(ticker, target_years, selected_concepts)

csv_file = "finance_companies.csv"
process_all_tickers(csv_file)
