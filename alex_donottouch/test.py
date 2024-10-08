import xml.etree.ElementTree as ET
from datetime import datetime
import pandas as pd

def clean_heart_rate_data(file_path, start_date_str, end_date_str):
    # Parse the XML from the file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Define the start and end dates for filtering and convert to date objects
    start_filter_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
    end_filter_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

    # Extract relevant fields for only heart rate records
    cleaned_data = []
    for record in root.findall('Record'):
        record_type = record.get('type')
        record_value = record.get('value')
        start_date = record.get('startDate')
        end_date = record.get('endDate')

        # Convert the startDate and endDate to datetime objects (with timezone info)
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S %z")
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S %z")

        # Check if the record is a heart rate record and falls within the date range
        if record_type == "HKQuantityTypeIdentifierHeartRate" and start_filter_date <= start_date_dt.date() <= end_filter_date:
            cleaned_data.append({
                'type': record_type,
                'value': record_value,
                'startDate': start_date_dt,
                'endDate': end_date_dt,
            })

    return cleaned_data

if __name__ == "__main__":
    # File path to your Apple Health export file
    file_path = "/Users/alexdang/ihealth.ai/apple_health_export/export.xml"
    
    # Define the date range for filtering
    start_date_str = "2024-09-19"
    end_date_str = "2024-09-20"
    
    # Clean the heart rate data
    cleaned_heart_rate_data = clean_heart_rate_data(file_path, start_date_str, end_date_str)
    
    # If no records found, print a message
    if not cleaned_heart_rate_data:
        print("No heart rate records found within the specified date range.")
    
    # Convert to Pandas DataFrame for further analysis or saving to CSV
    df = pd.DataFrame(cleaned_heart_rate_data)
    
    # Print the DataFrame to check the records
    print(df)
    
    # Optionally, save to CSV if the DataFrame is not empty
    if not df.empty:
        df.to_csv('cleaned_heart_rate_data.csv', index=False)
        print("Heart rate data successfully saved to 'cleaned_heart_rate_data.csv'.")
    else:
        print("The DataFrame is empty. No data to write.")
