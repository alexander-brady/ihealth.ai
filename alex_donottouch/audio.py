import pandas as pd
import json
import os

def analyze_audio_exposure(file_path, output_directory):
    # Load the data from the CSV file
    data = pd.read_csv(file_path)

    # Filter only for Headphone Audio Exposure data
    audio_data = data[data['type'] == 'HKQuantityTypeIdentifierHeadphoneAudioExposure']

    # Convert startDate to datetime for easier analysis
    audio_data['startDate'] = pd.to_datetime(audio_data['startDate'])

    # Get key stats
    average_exposure = audio_data['value'].mean()
    min_exposure = audio_data['value'].min()
    max_exposure = audio_data['value'].max()

    # Group data by day and average the audio exposure for each day
    daily_exposure_avg = audio_data.groupby(audio_data['startDate'].dt.date)['value'].mean()

    # Convert the index (dates) to strings for JSON serialization
    daily_exposure_avg = daily_exposure_avg.rename(index=str)

    # Find the highest and lowest exposure day (using averages)
    highest_exposure_day = daily_exposure_avg.idxmax()
    highest_exposure_value = daily_exposure_avg.max()
    
    lowest_exposure_day = daily_exposure_avg.idxmin()
    lowest_exposure_value = daily_exposure_avg.min()

    # Create a dictionary to hold the analysis
    audio_analysis = {
        "average_exposure_per_record": average_exposure,
        "min_exposure_per_record": min_exposure,
        "max_exposure_per_record": max_exposure,
        "daily_audio_exposure_avg_summary": daily_exposure_avg.to_dict(),
        "highest_exposure_day": str(highest_exposure_day),
        "highest_exposure_value": highest_exposure_value,
        "lowest_exposure_day": str(lowest_exposure_day),
        "lowest_exposure_value": lowest_exposure_value,
        "medical_comments": []
    }

    # Adding medical comments based on the analysis
    medical_comment = ""

    # Thresholds based on WHO recommendations
    if average_exposure > 70:
        medical_comment += "Your average headphone audio exposure exceeds 70 dB, which is the recommended limit to avoid hearing damage. Consider lowering the volume for prolonged listening sessions.\n"
    else:
        medical_comment += "Your average audio exposure is within the safe range recommended by health organizations.\n"

    # Observing any exposure spikes or declines
    if max_exposure > 85:
        medical_comment += "You have records of exposure exceeding 85 dB, which can cause hearing damage if sustained for long periods. Please reduce the volume in future listening sessions.\n"

    # Breakdown of exposure data and additional comments
    breakdown_comment = f"Highest Audio Exposure Day: {highest_exposure_day} with an average of {highest_exposure_value:.2f} dB. This suggests prolonged or high-volume listening sessions."
    breakdown_comment += f"\nLowest Audio Exposure Day: {lowest_exposure_day} with an average of {lowest_exposure_value:.2f} dB, possibly reflecting a day of less or no headphone use."
    
    # Weekday vs Weekend analysis
    audio_data['weekday'] = audio_data['startDate'].dt.weekday
    weekday_exposure = audio_data[audio_data['weekday'] < 5]['value'].mean()
    weekend_exposure = audio_data[audio_data['weekday'] >= 5]['value'].mean()

    if weekday_exposure > weekend_exposure:
        breakdown_comment += f"\nYou tend to use your headphones more on weekdays with an average exposure of {weekday_exposure:.2f} dB compared to {weekend_exposure:.2f} dB on weekends."
    else:
        breakdown_comment += f"\nYou tend to use your headphones more on weekends with an average exposure of {weekend_exposure:.2f} dB compared to {weekday_exposure:.2f} dB on weekdays."

    # Add medical comments and breakdown to the analysis
    audio_analysis['medical_comments'].extend([medical_comment, breakdown_comment])

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Save analysis to a JSON file in the specified directory
    output_file = os.path.join(output_directory, "audio_exposure_analysis.json")
    with open(output_file, 'w') as json_file:
        json.dump(audio_analysis, json_file, indent=4)

    # Print summary statistics and medical comments
    print(f"Average Exposure per Record: {average_exposure:.2f} dB")
    print(f"Minimum Exposure in a Record: {min_exposure:.2f} dB")
    print(f"Maximum Exposure in a Record: {max_exposure:.2f} dB")

    print("\nDaily Audio Exposure (Average) Summary:")
    print(daily_exposure_avg)

    print("\nMedical Comments:")
    for comment in audio_analysis['medical_comments']:
        print(comment)

if __name__ == "__main__":
    # Path to your cleaned data CSV
    file_path = "/Users/alexdang/ihealth.ai/cleaned_data_by_date.csv"
    output_directory = "/Users/alexdang/ihealth.ai/data"
    
    # Analyze headphone audio exposure data
    analyze_audio_exposure(file_path, output_directory)
