import pandas as pd

# Load the CSV file into a pandas DataFrame
file_path = '/Users/alexdang/ihealth.ai/cleaned_data_by_date.csv'
df = pd.read_csv(file_path)

# Convert the 'value' column to numeric (in case there are any non-numeric values)
df['value'] = pd.to_numeric(df['value'], errors='coerce')

# Group by 'type' and aggregate the 'value' column
# Aggregating with mean, sum, min, and max
aggregated_data = df.groupby('type').agg({
    'value': ['mean', 'sum', 'min', 'max'],
    'startDate': 'min',  # Get the earliest start date for each type
    'endDate': 'max'     # Get the latest end date for each type
})

# Flatten the column names for easier use
aggregated_data.columns = ['_'.join(col).strip() for col in aggregated_data.columns.values]

# Display the aggregated data
print(aggregated_data)

# Optionally, save the aggregated data to a new CSV file
aggregated_data.to_csv('/Users/alexdang/ihealth.ai/aggregated_data.csv')
