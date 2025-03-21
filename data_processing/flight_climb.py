import pandas as pd
import json
import os

def analyze_flights_climbed(file_path, output_directory):
    # Load the data from the CSV file
    data = pd.read_csv(file_path)

    # Filter only for Flights Climbed data
    flights_data = data[data['type'] == 'HKQuantityTypeIdentifierFlightsClimbed']

    # Convert startDate to datetime for easier analysis
    flights_data['startDate'] = pd.to_datetime(flights_data['startDate'])

    # Get key stats
    total_flights_climbed = flights_data['value'].sum()
    average_flights_climbed = flights_data['value'].mean()
    min_flights_climbed = flights_data['value'].min()
    max_flights_climbed = flights_data['value'].max()

    # Group data by day and sum the flights climbed for each day
    daily_flights_climbed = flights_data.groupby(flights_data['startDate'].dt.date)['value'].sum()

    # Convert the index (dates) to strings for JSON serialization
    daily_flights_climbed = daily_flights_climbed.rename(index=str)

    # Find the highest and lowest flights climbed day
    highest_flights_day = daily_flights_climbed.idxmax()
    highest_flights_value = daily_flights_climbed.max()
    
    lowest_flights_day = daily_flights_climbed.idxmin()
    lowest_flights_value = daily_flights_climbed.min()

    # Create a dictionary to hold the analysis
    flights_analysis = {
        "total_flights_climbed": total_flights_climbed,
        "average_flights_climbed_per_record": average_flights_climbed,
        "min_flights_climbed_per_record": min_flights_climbed,
        "max_flights_climbed_per_record": max_flights_climbed,
        "daily_flights_climbed_summary": daily_flights_climbed.to_dict(),
        "highest_flights_day": str(highest_flights_day),
        "highest_flights_value": highest_flights_value,
        "lowest_flights_day": str(lowest_flights_day),
        "lowest_flights_value": lowest_flights_value,
        "medical_comments": []
    }

    # Adding medical comments based on the analysis
    medical_comment = ""

    # General fitness comment on flights climbed
    if total_flights_climbed < 5:
        medical_comment += "Your total flights climbed is quite low. It's recommended to aim for more stair climbing, as it strengthens legs and increases cardiovascular fitness.\n"
    elif total_flights_climbed > 20:
        medical_comment += "You've climbed a significant number of flights! Stair climbing is a great way to boost fitness and improve heart health.\n"
    
    # Observing highest and lowest activity
    breakdown_comment = f"Highest Flights Climbed Day: {highest_flights_day} with {highest_flights_value} flights climbed."
    breakdown_comment += f"\nLowest Flights Climbed Day: {lowest_flights_day} with {lowest_flights_value} flights climbed. Consider adding more stair climbing to your routine for better health benefits."

    # Add medical comments and breakdown to the analysis
    flights_analysis['medical_comments'].extend([medical_comment, breakdown_comment])

    # Ensure the output directory exists
    os.makedirs(output_directory, exist_ok=True)

    # Save analysis to a JSON file in the specified directory
    output_file = os.path.join(output_directory, "flights_climbed_analysis.json")
    with open(output_file, 'w') as json_file:
        json.dump(flights_analysis, json_file, indent=4)

    # Print summary statistics and medical comments
    print(f"Total Flights Climbed: {total_flights_climbed}")
    print(f"Average Flights Climbed per Record: {average_flights_climbed}")
    print(f"Minimum Flights Climbed in a Record: {min_flights_climbed}")
    print(f"Maximum Flights Climbed in a Record: {max_flights_climbed}")

    print("\nDaily Flights Climbed Summary:")
    print(daily_flights_climbed)

    print("\nMedical Comments:")
    for comment in flights_analysis['medical_comments']:
        print(comment)

if __name__ == "__main__":
    # Path to your cleaned data CSV
    file_path = "/Users/alexdang/ihealth.ai/cleaned_data_by_date.csv"
    output_directory = "/Users/alexdang/ihealth.ai/data"
    
    # Analyze flights climbed data
    analyze_flights_climbed(file_path, output_directory)
