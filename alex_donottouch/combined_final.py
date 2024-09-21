import pandas as pd

# Paths to the CSV files
combined_csv_path = '/Users/alexdang/ihealth.ai/data/combined_updated_health_data.csv'
sleep_analysis_csv_path = '/Users/alexdang/ihealth.ai/data/updated_sleep_analysis_data.csv'

# Load the combined CSV (step count data) into a DataFrame
combined_df = pd.read_csv(combined_csv_path)

# Load the sleep analysis CSV into a DataFrame
sleep_df = pd.read_csv(sleep_analysis_csv_path)

# Merge the dataframes by appending the sleep analysis data
# Assuming we want to align the sleep data as new rows with a new column `sleepDurationHours`
# We will fill the 'value' column for sleep data with NaN
sleep_df['value'] = pd.NA

# Concatenate the two DataFrames
final_combined_df = pd.concat([combined_df, sleep_df], ignore_index=True)

# Save the final combined data into a new CSV file
output_csv = '/Users/alexdang/ihealth.ai/data/final_combined_health_data.csv'
final_combined_df.to_csv(output_csv, index=False)

print(f"Final combined data (with sleep analysis) saved to {output_csv}")
