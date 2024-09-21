import xml.etree.ElementTree as ET
from datetime import datetime
import pandas as pd

def clean_data_by_date(file_path, start_date_str, end_date_str):
    # Parse the XML from the file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Define the start and end dates for filtering (offset-naive)
    start_filter_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_filter_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    # Extract relevant fields for all records
    cleaned_data = []
    for record in root.findall('Record'):
        record_type = record.get('type')
        record_value = record.get('value')
        start_date = record.get('startDate')
        end_date = record.get('endDate')

        # Convert the startDate and endDate to datetime objects, then remove timezone info (offset-naive)
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S %z").replace(tzinfo=None)
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S %z").replace(tzinfo=None)

        # Check if the record falls within the date range
        if start_filter_date <= start_date_dt <= end_filter_date:
            cleaned_data.append({
                'type': record_type,
                'value': record_value,
                'startDate': start_date,
                'endDate': end_date,
            })

    return cleaned_data

if __name__ == "__main__":
    # File path to your Apple Health export file
    file_path = "/Users/alexdang/ihealth.ai/export.xml"
    
    # Define the date range for filtering
    start_date_str = "2024-08-23"
    end_date_str = "2024-09-19"
    
    # Clean the data
    cleaned_output = clean_data_by_date(file_path, start_date_str, end_date_str)
    
    # If no records found, print a message
    if not cleaned_output:
        print("No records found within the specified date range.")
    
    # Convert to Pandas DataFrame for further analysis or saving to CSV
    df = pd.DataFrame(cleaned_output)
    
    # Print the DataFrame to check the records
    print(df)
    
    # Optionally, save to CSV if the DataFrame is not empty
    if not df.empty:
        df.to_csv('cleaned_data_by_date.csv', index=False)
        print("Data successfully saved to 'cleaned_data_by_date.csv'.")
    else:
        print("The DataFrame is empty. No data to write.")
