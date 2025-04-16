import pickle
import os

# Define the ticker to match the saved file
ticker = "ALL"
directory_path = "pkl_files"  # Replace with your directory path

# Combine the directory path and filename to get the full path
filename = os.path.join(directory_path, f"{ticker}_financials.pkl")

# Load the dictionary from the pickle file
with open(filename, "rb") as f:
    loaded_data = pickle.load(f)

# Print the loaded data with their types
print(f"Loaded Data from {filename}:")
for key, value in loaded_data.items():
    print(f"{key}: {value} (Type: {type(value).__name__})")
# in a directory so it isn't reading properly. next steps put these new vars in the treemap on the app.py file and then test if it works.
# then if it works load in all the companies and hoorayyy!!!!!!!!!!!