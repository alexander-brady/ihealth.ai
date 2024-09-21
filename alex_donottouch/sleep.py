import xml.etree.ElementTree as ET
from datetime import datetime
import pandas as pd

def clean_sleep_analysis_data(file_path, start_date_str, end_date_str):
    # Parse the XML from the file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Define the start and end dates for filtering
    start_filter_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_filter_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    # Extract relevant fields for only sleep analysis records
    cleaned_data = []
    for record in root.findall('Record'):
        record_type = record.get('type')
        start_date = record.get('startDate')
        end_date = record.get('endDate')

        # Check if the record is a sleep analysis record
        if record_type == "HKCategoryTypeIdentifierSleepAnalysis":
            # Convert the startDate and endDate to datetime objects, removing timezone info
            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S %z").replace(tzinfo=None)
            end_date_dt = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S %z").replace(tzinfo=None)

            # Check if the record falls within the specified date range
            if start_filter_date <= start_date_dt <= end_filter_date:
                # Calculate the duration of time spent in bed
                sleep_duration = (end_date_dt - start_date_dt).total_seconds() / 3600  # in hours

                cleaned_data.append({
                    'type': record_type,
                    'startDate': start_date_dt,
                    'endDate': end_date_dt,
                    'sleepDurationHours': sleep_duration
                })

    return cleaned_data

if __name__ == "__main__":
    # File path to your Apple Health export file
    file_path = "/Users/alexdang/ihealth.ai/workout-routes/export.xml"
    
    # Define the date range for filtering
    start_date_str = "2020-01-07"
    end_date_str = "2020-03-12"
    
    # Clean the sleep analysis data
    cleaned_sleep_data = clean_sleep_analysis_data(file_path, start_date_str, end_date_str)
    
    # If no records found, print a message
    if not cleaned_sleep_data:
        print("No sleep analysis records found within the specified date range.")
    
    # Convert to Pandas DataFrame for further analysis or saving to CSV
    df = pd.DataFrame(cleaned_sleep_data)
    
    # Print the DataFrame to check the records
    print(df)
    
    # Optionally, save to CSV if the DataFrame is not empty
    if not df.empty:
        output_path = "/Users/alexdang/ihealth.ai/data/cleaned_sleep_analysis_data.csv"
        df.to_csv(output_path, index=False)
        print(f"Sleep analysis data successfully saved to '{output_path}'.")
    else:
        print("The DataFrame is empty. No data to write.")
