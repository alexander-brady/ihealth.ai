import pandas as pd

# Paths to the CSV files
non_sleep_csv = '/Users/alexdang/ihealth.ai/cleaned_data_by_date.csv'
heart_rate_csv = '/Users/alexdang/ihealth.ai/cleaned_heart_rate_data.csv'

# Read the CSVs into DataFrames
non_sleep_df = pd.read_csv(non_sleep_csv)
heart_rate_df = pd.read_csv(heart_rate_csv)

# Use pd.concat() to combine the data
combined_df = pd.concat([non_sleep_df, heart_rate_df], ignore_index=True)

# Save the combined data into a new CSV file
output_csv = '/Users/alexdang/ihealth.ai/data/combined_updated_health_data.csv'
combined_df.to_csv(output_csv, index=False)

print(f"Combined data (including heart rate) saved to {output_csv}")
