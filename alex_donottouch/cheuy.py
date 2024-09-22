from pymongo import MongoClient
from datetime import datetime

# MongoDB setup
MONGO_URI = ""
client = MongoClient(MONGO_URI)
db = client['health_data']
sleep_analysis_collection = db['combined_health_metrics_Pokemon']

def list_sleep_data_before_cutoff(cutoff_date_str="2024-09-19"):
    # Define the cutoff date
    cutoff_date = datetime.strptime(cutoff_date_str, "%Y-%m-%d")
    
    # Query the sleep data from MongoDB up to the cutoff date, assuming endDate is stored as a string
    sleep_data = list(sleep_analysis_collection.find({
        "type": "HKCategoryTypeIdentifierSleepAnalysis"
    }))
    
    # Prepare the data for printing or feeding into LLM
    formatted_sleep_data = []
    for record in sleep_data:
        try:
            # Convert the endDate string to a datetime object for comparison
            end_date = datetime.strptime(record.get("endDate"), "%Y-%m-%d %H:%M:%S")
            
            # Only include records with endDate before the cutoff
            if end_date <= cutoff_date:
                formatted_sleep_data.append({
                    "startDate": record.get("startDate"),
                    "endDate": record.get("endDate"),
                    "sleepDurationHours": record.get("sleepDurationHours")
                })
        except Exception as e:
            print(f"Error processing record: {e}")
    
    return formatted_sleep_data

# Example usage
def feed_sleep_data_to_llm():
    sleep_data_for_llm = list_sleep_data_before_cutoff()  # Get sleep data up to the cutoff date
    # Print for debugging purposes
    for data in sleep_data_for_llm:
        print(f"Start Date: {data['startDate']}, End Date: {data['endDate']}, Sleep Duration: {data['sleepDurationHours']} hours")
    
    return sleep_data_for_llm

if __name__ == '__main__':
    feed_sleep_data_to_llm()
