import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import pandas as pd

# Function to clean sleep analysis data from the XML file
def clean_sleep_analysis_data(root, start_date_str, end_date_str):
    start_filter_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_filter_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    cleaned_data = []
    for record in root.findall('Record'):
        record_type = record.get('type')
        start_date = record.get('startDate')
        end_date = record.get('endDate')

        if record_type == "HKCategoryTypeIdentifierSleepAnalysis":
            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S %z").replace(tzinfo=None)
            end_date_dt = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S %z").replace(tzinfo=None)

            if start_filter_date <= start_date_dt <= end_filter_date:
                sleep_duration = (end_date_dt - start_date_dt).total_seconds() / 3600  # in hours

                cleaned_data.append({
                    'type': record_type,
                    'value': None,  # Sleep analysis records do not have a "value"
                    'startDate': start_date_dt,
                    'endDate': end_date_dt,
                    'sleepDurationHours': sleep_duration
                })

    return cleaned_data

# Function to clean other health data (non-sleep analysis) from the XML file
def clean_other_health_data(root, start_date_str, end_date_str):
    start_filter_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    end_filter_date = datetime.strptime(end_date_str, "%Y-%m-%d")

    cleaned_data = []
    for record in root.findall('Record'):
        record_type = record.get('type')
        record_value = record.get('value')
        start_date = record.get('startDate')
        end_date = record.get('endDate')

        # Ensure the record is not a sleep analysis record and has a numeric value
        if record_type != "HKCategoryTypeIdentifierSleepAnalysis" and record_value.isdigit():
            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S %z").replace(tzinfo=None)
            end_date_dt = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S %z").replace(tzinfo=None)

            if start_filter_date <= start_date_dt <= end_filter_date:
                cleaned_data.append({
                    'type': record_type,
                    'value': float(record_value),  # Convert value to float
                    'startDate': start_date_dt,
                    'endDate': end_date_dt,
                    'sleepDurationHours': None  # Non-sleep records do not have sleep duration
                })

    return cleaned_data

# Function to update dates for sleep analysis records
def update_sleep_analysis_dates(data, new_start_date_str):
    new_start_date = datetime.strptime(new_start_date_str, "%Y-%m-%d")
    time_deltas = data['endDate'] - data['startDate']

    new_start_dates = [new_start_date]
    new_end_dates = [new_start_date + time_deltas.iloc[0]]

    for i in range(1, len(data)):
        new_start_dates.append(new_end_dates[-1] + timedelta(seconds=1))  # Avoid overlap
        new_end_dates.append(new_start_dates[-1] + time_deltas.iloc[i])

    data['startDate'] = new_start_dates
    data['endDate'] = new_end_dates

    return data

# Combined function that first cleans the XML data and then updates the dates
def clean_and_update_sleep_data(xml_file_path, start_date_str, end_date_str, new_start_date_str):
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    # Clean the sleep analysis data from the XML
    cleaned_sleep_data = clean_sleep_analysis_data(root, start_date_str, end_date_str)
    
    # Clean other health data from the XML
    cleaned_other_health_data = clean_other_health_data(root, start_date_str, end_date_str)

    # Combine both datasets
    combined_data = cleaned_sleep_data + cleaned_other_health_data

    # Convert combined data to a DataFrame
    df = pd.DataFrame(combined_data)

    # Separate the sleep data for date updating
    sleep_data_df = df[df['type'] == "HKCategoryTypeIdentifierSleepAnalysis"]

    # Update the dates in the cleaned sleep data
    updated_sleep_df = update_sleep_analysis_dates(sleep_data_df, new_start_date_str)

    # Combine the updated sleep data with the non-sleep data
    final_df = pd.concat([updated_sleep_df, df[df['type'] != "HKCategoryTypeIdentifierSleepAnalysis"]])

    # Save the final updated data to CSV
    output_path = "/Users/alexdang/ihealth.ai/data/combined_updated_data.csv"
    final_df.to_csv(output_path, index=False)
    print(f"Combined and updated health data saved to '{output_path}'.")

if __name__ == "__main__":
    xml_file_path = "/Users/alexdang/ihealth.ai/workout-routes/export.xml"
    start_date_str = "2020-01-07"
    end_date_str = "2020-03-12"
    new_start_date_str = "2024-08-23"
    
    clean_and_update_sleep_data(xml_file_path, start_date_str, end_date_str, new_start_date_str)
