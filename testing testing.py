import pickle

# Define the ticker to match the saved file
ticker = "JPM"
filename = f"{ticker}_deposits.pkl"

# Load the dictionary from the pickle file
with open(filename, "rb") as f:
    loaded_data = pickle.load(f)

# Print the loaded data with their types
print(f"Loaded Data from {filename}:")
for key, value in loaded_data.items():
    print(f"{key}: {value} (Type: {type(value).__name__})")
