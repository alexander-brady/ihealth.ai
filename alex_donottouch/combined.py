import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import pandas as pd

# Function to clean all non-sleep health data (like heart rate, step count) from the XML
def clean_data_by_date(file_path, start_date_str, end_date_str):
    # Parse the XML from the file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Define the start and end dates for filtering (offset-naive)
    start_filter_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_filter_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    # Extract relevant fields for all records except sleep analysis
    cleaned_data = []
    for record in root.findall('Record'):
        record_type = record.get('type')
        record_value = record.get('value')
        start_date = record.get('startDate')
        end_date = record.get('endDate')

        # Convert the startDate and endDate to datetime objects, then remove timezone info (offset-naive)
        start_date_dt = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S %z").replace(tzinfo=None)
        end_date_dt = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S %z").replace(tzinfo=None)

        # Check if the record is not sleep data and falls within the date range
        if record_type != "HKCategoryTypeIdentifierSleepAnalysis" and start_filter_date <= start_date_dt <= end_filter_date:
            cleaned_data.append({
                'type': record_type,
                'value': record_value,
                'startDate': start_date_dt,
                'endDate': end_date_dt,
            })

    return cleaned_data

# Function to clean sleep analysis data and shift dates
def clean_sleep_analysis_data_and_shift(file_path, start_date_str, end_date_str, new_start_date_str):
    # Parse the XML from the file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Define the start and end dates for filtering
    start_filter_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_filter_date = datetime.strptime(end_date_str, "%Y-%m-%d")
    new_start_date = datetime.strptime(new_start_date_str, "%Y-%m-%d")

    # Extract relevant fields for sleep analysis records
    cleaned_data = []
    for record in root.findall('Record'):
        record_type = record.get('type')
        start_date = record.get('startDate')
        end_date = record.get('endDate')

        # Check if the record is a sleep analysis record
        if record_type == "HKCategoryTypeIdentifierSleepAnalysis":
            # Convert startDate and endDate to datetime, remove timezone info
            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S %z").replace(tzinfo=None)
            end_date_dt = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S %z").replace(tzinfo=None)

            # Ensure it falls within the old date range
            if start_filter_date <= start_date_dt <= end_filter_date:
                # Calculate the duration of time spent in bed
                sleep_duration = (end_date_dt - start_date_dt).total_seconds() / 3600  # in hours

                cleaned_data.append({
                    'type': record_type,
                    'startDate': start_date_dt,
                    'endDate': end_date_dt,
                    'sleepDurationHours': sleep_duration
                })

    # Convert to DataFrame
    df = pd.DataFrame(cleaned_data)
    
    # Shift the sleep analysis dates by day starting from the new start date
    if not df.empty:
        # Extract original durations (endDate - startDate)
        time_deltas = df['endDate'] - df['startDate']

        # Shift dates: Assign new start dates starting from the new start date, increasing by a day for each entry
        new_start_dates = [new_start_date]
        new_end_dates = [new_start_date + time_deltas.iloc[0]]

        for i in range(1, len(df)):
            next_day = new_start_dates[-1] + timedelta(days=1)
            new_start_dates.append(next_day)
            new_end_dates.append(next_day + time_deltas.iloc[i])

        # Update the DataFrame with new dates
        df['startDate'] = new_start_dates
        df['endDate'] = new_end_dates

    return df

# Combined function that processes non-sleep and sleep data separately
def clean_and_update_health_data(xml_file_path, non_sleep_start_date_str, non_sleep_end_date_str, sleep_start_date_str, sleep_end_date_str, new_sleep_start_date_str):
    # Clean non-sleep health data (keeps original dates)
    cleaned_non_sleep_data = clean_data_by_date(xml_file_path, non_sleep_start_date_str, non_sleep_end_date_str)

    # Clean and shift sleep analysis data
    cleaned_sleep_data = clean_sleep_analysis_data_and_shift(xml_file_path, sleep_start_date_str, sleep_end_date_str, new_sleep_start_date_str)
    
    # Convert cleaned non-sleep data to a DataFrame
    non_sleep_df = pd.DataFrame(cleaned_non_sleep_data)
    
    # Combine sleep data and non-sleep data
    final_df = pd.concat([cleaned_sleep_data, non_sleep_df], ignore_index=True)

    # Save the combined data to CSV
    output_path = "/Users/alexdang/ihealth.ai/data/combined_updated_health_data.csv"
    final_df.to_csv(output_path, index=False)
    print(f"Combined and updated health data saved to '{output_path}'.")

if __name__ == "__main__":
    # File path to your Apple Health XML export file
    xml_file_path = "/Users/alexdang/ihealth.ai/workout-routes/export.xml"
    
    # Define the date range for non-sleep data (keep these dates as they are)
    non_sleep_start_date_str = "2024-08-23"
    non_sleep_end_date_str = "2024-09-19"
    
    # Define the old date range for sleep analysis (shift these dates)
    sleep_start_date_str = "2020-01-07"
    sleep_end_date_str = "2020-03-12"
    
    # Define the new start date for updating the sleep analysis records
    new_sleep_start_date_str = "2024-08-23"
    
    # Clean and update all health data
    clean_and_update_health_data(xml_file_path, non_sleep_start_date_str, non_sleep_end_date_str, sleep_start_date_str, sleep_end_date_str, new_sleep_start_date_str)
