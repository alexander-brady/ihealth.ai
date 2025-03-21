# combined.py

import xml.etree.ElementTree as ET
from datetime import datetime
import pandas as pd
from test import clean_heart_rate_data  # Import the heart rate function from test.py

# Function to clean non-sleep data
def clean_data_by_date(file_path, start_date_str, end_date_str):
    tree = ET.parse(file_path)
    root = tree.getroot()

    start_filter_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_filter_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    cleaned_data = []
    for record in root.findall('Record'):
        record_type = record.get('type')
        record_value = record.get('value')
        start_date = record.get('startDate')
        end_date = record.get('endDate')

        # Convert startDate and endDate to datetime objects and strip timezone info
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S %z").replace(tzinfo=None)
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S %z").replace(tzinfo=None)

        # Check if the record is not sleep data and falls within the date range
        if start_filter_date <= start_date_dt <= end_filter_date:
            cleaned_data.append({
                'type': record_type,
                'value': record_value,
                'startDate': start_date_dt,
                'endDate': end_date_dt,
            })
    
    return cleaned_data

# Combined function to process non-sleep and heart rate data and merge them
def clean_and_update_health_data(xml_file_path, non_sleep_start_date_str, non_sleep_end_date_str, heart_rate_start_date_str, heart_rate_end_date_str):
    print("Processing non-sleep data...")
    cleaned_non_sleep_data = clean_data_by_date(xml_file_path, non_sleep_start_date_str, non_sleep_end_date_str)

    print("Processing heart rate data...")
    cleaned_heart_rate_data = clean_heart_rate_data(xml_file_path, heart_rate_start_date_str, heart_rate_end_date_str)  # Use the imported function

    # Convert to DataFrames
    non_sleep_df = pd.DataFrame(cleaned_non_sleep_data)
    heart_rate_df = pd.DataFrame(cleaned_heart_rate_data)

    # Debugging: Check if either dataset is empty
    if non_sleep_df.empty:
        print("Non-sleep data is empty!")
    if heart_rate_df.empty:
        print("Heart rate data is empty!")

    # Ensure both datasets exist before merging
    if non_sleep_df.empty or heart_rate_df.empty:
        print("Either non-sleep or heart rate data is missing.")
        return

    # Merge by date
    final_df = pd.merge_asof(
        non_sleep_df.sort_values('startDate'),
        heart_rate_df.sort_values('startDate'),
        left_on='startDate', right_on='startDate', direction='nearest',
        suffixes=('', '_heartRate')  # To avoid any column conflicts
    )

    # Save to CSV
    output_path = "/Users/alexdang/ihealth.ai/data/combined_updated_health_data_with_heart_rate.csv"
    final_df.to_csv(output_path, index=False)
    print(f"Combined health data saved to '{output_path}'")

if __name__ == "__main__":
    # File path to your Apple Health XML export file
    xml_file_path = "/Users/alexdang/ihealth.ai/workout-routes/export.xml"
    
    # Define the date range for non-sleep and heart rate data
    non_sleep_start_date_str = "2024-08-23"
    non_sleep_end_date_str = "2024-09-19"
    
    heart_rate_start_date_str = "2024-09-19"
    heart_rate_end_date_str = "2024-09-20"
    
    # Process and merge the data
    clean_and_update_health_data(xml_file_path, non_sleep_start_date_str, non_sleep_end_date_str, heart_rate_start_date_str, heart_rate_end_date_str)
