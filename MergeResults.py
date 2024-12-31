import pandas as pd

# Load the original input and formatted results CSV files
original_data = pd.read_csv("ItemsLupoWantsv2.csv")
formatted_results = pd.read_csv("formatted_results.csv")

# Add new columns for the low estimate value and methodology
original_data['Low Estimate Value'] = None
original_data['Summary of Methodology'] = None

# Merge formatted results into the original data
for index, row in formatted_results.iterrows():
    response_number = row['Response Number'] - 1  # Adjust for 0-based indexing
    # Parse the formatted result as a dictionary
    try:
        formatted_result = eval(row['Formatted Result'])  # Assuming JSON-like formatted string
        low_value = formatted_result.get("low_value", "")
        methodology = formatted_result.get("methodology", "")
    except Exception as e:
        low_value = "Error extracting data"
        methodology = str(e)

    # Update the original DataFrame
    original_data.at[response_number, 'Low Estimate Value'] = low_value
    original_data.at[response_number, 'Summary of Methodology'] = methodology

# Save the merged data to a new CSV file
original_data.to_csv("EstimatedItemValues.csv", index=False)
print("File saved as 'EstimatedItemValues.csv'")
