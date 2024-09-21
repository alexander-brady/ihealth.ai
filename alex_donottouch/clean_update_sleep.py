import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import pandas as pd

# Function to clean sleep analysis data from the XML file
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

# Function to update sleep analysis dates from a cleaned dataset
def update_sleep_analysis_dates(data, new_start_date_str):
    # Convert new_start_date_str to datetime
    new_start_date = datetime.strptime(new_start_date_str, "%Y-%m-%d")

    # Extract original durations (endDate - startDate)
    time_deltas = data['endDate'] - data['startDate']

    # Update startDate and endDate based on new start date
    new_start_dates = [new_start_date]
    new_end_dates = [new_start_date + time_deltas.iloc[0]]

    for i in range(1, len(data)):
        new_start_dates.append(new_end_dates[-1] + timedelta(seconds=1))  # Avoid overlap
        new_end_dates.append(new_start_dates[-1] + time_deltas.iloc[i])

    # Apply updated dates to the DataFrame
    data['startDate'] = new_start_dates
    data['endDate'] = new_end_dates

    return data

# Combined function that first cleans the XML data and then updates the dates
def clean_and_update_sleep_data(xml_file_path, start_date_str, end_date_str, new_start_date_str):
    # Clean the sleep analysis data from the XML
    cleaned_sleep_data = clean_sleep_analysis_data(xml_file_path, start_date_str, end_date_str)
    
    if not cleaned_sleep_data:
        print("No sleep analysis records found within the specified date range.")
        return

    # Convert cleaned data to a DataFrame
    df = pd.DataFrame(cleaned_sleep_data)

    # Update the dates in the cleaned sleep data
    updated_df = update_sleep_analysis_dates(df, new_start_date_str)

    # Save the updated data to CSV
    output_path = "/Users/alexdang/ihealth.ai/data/updated_sleep_analysis_data.csv"
    updated_df.to_csv(output_path, index=False)
    print(f"Updated sleep analysis data saved to '{output_path}'.")

if __name__ == "__main__":
    # File path to your Apple Health XML export file
    xml_file_path = "/Users/alexdang/ihealth.ai/workout-routes/export.xml"
    
    # Define the date range for cleaning the sleep analysis records
    start_date_str = "2020-01-07"
    end_date_str = "2020-03-12"
    
    # Define the new start date for updating the records
    new_start_date_str = "2024-08-23"
    
    # Clean and update the sleep analysis data
    clean_and_update_sleep_data(xml_file_path, start_date_str, end_date_str, new_start_date_str)
