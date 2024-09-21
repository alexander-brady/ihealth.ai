import pandas as pd

def analyze_step_data(file_path):
    # Load the data from the CSV file
    data = pd.read_csv(file_path)

    # Filter only for Step Count data
    step_data = data[data['type'] == 'HKQuantityTypeIdentifierStepCount']

    # Convert startDate to datetime for easier analysis
    step_data['startDate'] = pd.to_datetime(step_data['startDate'])

    # Get key stats
    total_steps = step_data['value'].sum()
    average_steps = step_data['value'].mean()
    min_steps = step_data['value'].min()
    max_steps = step_data['value'].max()

    # Group data by day and sum the step counts for each day
    daily_steps = step_data.groupby(step_data['startDate'].dt.date)['value'].sum()

    # Print summary statistics
    print(f"Total Steps: {total_steps}")
    print(f"Average Steps per Record: {average_steps}")
    print(f"Minimum Steps in a Record: {min_steps}")
    print(f"Maximum Steps in a Record: {max_steps}")

    print("\nDaily Step Summary:")
    print(daily_steps)

    # Adding medical comments based on the analysis
    medical_comments = ""
    
    # If total steps are very high or very low, add a medical observation.
    if total_steps < 5000:
        medical_comments += "\nMedical Comment: Your activity level is quite low. It's recommended to aim for at least 5,000 to 10,000 steps daily for maintaining health.\n"
    elif total_steps > 10000:
        medical_comments += "\nMedical Comment: You are very active! Maintaining over 10,000 steps per day is considered excellent for cardiovascular health and overall fitness.\n"
    else:
        medical_comments += "\nMedical Comment: Your step count is within the moderate activity range. Consider gradually increasing your step count to improve fitness.\n"

    # If there are big jumps or declines in activity on certain days
    if daily_steps.max() > 10000 and daily_steps.min() < 1000:
        medical_comments += "Observation: There are some significant fluctuations in your activity levels. Try to maintain consistency in your daily step count.\n"
    
    print(medical_comments)

if __name__ == "__main__":
    # Path to your cleaned data CSV
    file_path = "/Users/alexdang/ihealth.ai/cleaned_data_by_date.csv"
    
    # Analyze step data
    analyze_step_data(file_path)
