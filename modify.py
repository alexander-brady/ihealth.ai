import pandas as pd
from datetime import timedelta, datetime

def update_sleep_analysis_dates(file_path, start_date_str):
    # Load the data from the CSV file
    data = pd.read_csv(file_path, header=None)
    
    # Assign column names if they are not set
    data.columns = ['type', 'startDate', 'endDate', 'sleepDurationHours']

    # Convert startDate and endDate to datetime
    data['startDate'] = pd.to_datetime(data['startDate'])
    data['endDate'] = pd.to_datetime(data['endDate'])

    # Define the start date for modification
    start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
    
    # Calculate the time difference between consecutive rows
    time_deltas = data['endDate'] - data['startDate']
    
    # Update dates starting from the new start date
    new_start_dates = [start_date]
    new_end_dates = [start_date + time_deltas[0]]
    
    for i in range(1, len(data)):
        new_start_dates.append(new_end_dates[-1] + timedelta(seconds=1))  # Avoid overlap by adding 1 second
        new_end_dates.append(new_start_dates[-1] + time_deltas[i])

    # Update the DataFrame with new dates
    data['startDate'] = new_start_dates
    data['endDate'] = new_end_dates

    # Save the updated DataFrame to CSV
    output_path = "/Users/alexdang/ihealth.ai/data/updated_sleep_analysis_data.csv"
    data.to_csv(output_path, index=False, header=False)

    print(f"Updated sleep analysis data saved to '{output_path}'.")

if __name__ == "__main__":
    # Path to your cleaned sleep analysis CSV file
    file_path = "/Users/alexdang/ihealth.ai/data/cleaned_sleep_analysis_data.csv"
    
    # Define the new start date
    start_date_str = "2024-08-23"
    
    # Update the sleep analysis dates
    update_sleep_analysis_dates(file_path, start_date_str)
