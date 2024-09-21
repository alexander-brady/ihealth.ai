import pandas as pd
import json

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

    # Convert the index (dates) to strings to handle JSON serialization
    daily_steps = daily_steps.rename(index=str)

    # Find the highest and lowest activity day
    highest_activity_day = daily_steps.idxmax()
    highest_activity_steps = daily_steps.max()
    
    lowest_activity_day = daily_steps.idxmin()
    lowest_activity_steps = daily_steps.min()

    # Analyze weekend vs weekday activity
    step_data['weekday'] = step_data['startDate'].dt.weekday
    weekday_steps = step_data[step_data['weekday'] < 5]['value'].sum()
    weekend_steps = step_data[step_data['weekday'] >= 5]['value'].sum()

    # Create a dictionary to hold the analysis
    step_analysis = {
        "total_steps": total_steps,
        "average_steps_per_record": average_steps,
        "min_steps_per_record": min_steps,
        "max_steps_per_record": max_steps,
        "daily_step_summary": daily_steps.to_dict(),
        "highest_activity_day": str(highest_activity_day),
        "highest_activity_steps": highest_activity_steps,
        "lowest_activity_day": str(lowest_activity_day),
        "lowest_activity_steps": lowest_activity_steps,
        "weekday_steps": weekday_steps,
        "weekend_steps": weekend_steps,
        "medical_comments": []
    }

    # Adding medical comments based on the analysis
    medical_comment = ""

    if total_steps < 5000:
        medical_comment += "Your activity level is quite low. It's recommended to aim for at least 5,000 to 10,000 steps daily for maintaining health.\n"
    elif total_steps > 10000:
        medical_comment += "You are very active! Maintaining over 10,000 steps per day is considered excellent for cardiovascular health and overall fitness.\n"
    else:
        medical_comment += "Your step count is within the moderate activity range. Consider gradually increasing your step count to improve fitness.\n"

    if daily_steps.max() > 10000 and daily_steps.min() < 1000:
        medical_comment += "There are significant fluctuations in your activity levels. Try to maintain consistency in your daily step count.\n"

    # Breakdown of step data and additional comments
    breakdown_comment = f"Highest Activity Day: {highest_activity_day} with {highest_activity_steps} steps. This exceeds the recommended daily goal of 10,000 steps, indicating a particularly active day."
    breakdown_comment += f"\nLowest Activity Day: {lowest_activity_day} with only {lowest_activity_steps} steps. This could indicate a rest day or less mobility."
    
    # Weekday vs Weekend analysis
    if weekday_steps > weekend_steps:
        breakdown_comment += f"\nYou are generally more active on weekdays with {weekday_steps} steps compared to {weekend_steps} steps on weekends."
    else:
        breakdown_comment += f"\nYou are more active on weekends with {weekend_steps} steps compared to {weekday_steps} steps on weekdays."

    # Consistency and variability analysis
    consistency_comment = f"\nYou are generally consistent with an active lifestyle, frequently hitting 5,000-10,000 steps. However, you have some sedentary days, such as {lowest_activity_day}. Try to aim for more regular activity."
    variability_comment = "Large spikes in activity (e.g., over 10,000 steps on certain days) suggest intermittent high-intensity activities. Try balancing these spikes with regular movement on lower-step days."

    # Save analysis to a JSON file
    step_analysis['medical_comments'].extend([medical_comment, breakdown_comment, consistency_comment, variability_comment])

    output_file = file_path.replace(".csv", "_step_analysis_with_insights.json")
    with open(output_file, 'w') as json_file:
        json.dump(step_analysis, json_file, indent=4)

    # Print summary statistics and medical comments
    print(f"Total Steps: {total_steps}")
    print(f"Average Steps per Record: {average_steps}")
    print(f"Minimum Steps in a Record: {min_steps}")
    print(f"Maximum Steps in a Record: {max_steps}")

    print("\nDaily Step Summary:")
    print(daily_steps)

    print("\nMedical Comments:")
    for comment in step_analysis['medical_comments']:
        print(comment)

if __name__ == "__main__":
    # Path to your cleaned data CSV
    file_path = "/Users/alexdang/ihealth.ai/cleaned_data_by_date.csv"
    
    # Analyze step data
    analyze_step_data(file_path)
