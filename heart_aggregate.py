import pandas as pd

# File path to the cleaned heart rate data CSV
file_path = '/Users/alexdang/ihealth.ai/cleaned_heart_rate_data.csv'

# Read the CSV file into a pandas DataFrame
df = pd.read_csv(file_path)

# Convert the startDate and endDate columns to datetime (if they exist in your CSV)
df['startDate'] = pd.to_datetime(df['startDate'], errors='coerce')
df['endDate'] = pd.to_datetime(df['endDate'], errors='coerce')

# Perform the aggregation
aggregated_data = {
    "type": "HKQuantityTypeIdentifierHeartRate",
    "value_mean": df['value'].mean(),
    "value_sum": df['value'].sum(),
    "value_min": df['value'].min(),
    "value_max": df['value'].max(),
    "startDate_min": df['startDate'].min(),
    "endDate_max": df['endDate'].max(),
}

# Convert the aggregated data to a DataFrame for display
aggregated_df = pd.DataFrame([aggregated_data])

# Display the aggregated data
print(aggregated_df)

# Optionally save the aggregated data to a new CSV file
aggregated_df.to_csv('aggregated_heart_rate_data.csv', index=False)
print("Aggregated data saved to 'aggregated_heart_rate_data.csv'.")
