import xml.etree.ElementTree as ET
from pymongo import MongoClient

def clean_health_data(file_path):
    # Parse the XML from the file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extract relevant fields for sleep analysis, walking/running distance, and step count
    cleaned_data = []
    for record in root.findall('Record'):
        record_type = record.get('type')
        record_value = record.get('value')
        start_date = record.get('startDate')
        end_date = record.get('endDate')
        
        # Process specific health records
        if record_type in ["HKCategoryTypeIdentifierSleepAnalysis", "HKQuantityTypeIdentifierDistanceWalkingRunning", "HKQuantityTypeIdentifierStepCount"]:
            cleaned_data.append({
                'type': record_type,
                'value': record_value,
                'startDate': start_date,
                'endDate': end_date
            })

    return cleaned_data

def push_to_mongo(data):
    # Replace <db_password> with your actual password in the connection string
    client = MongoClient('mongodb+srv://alexjbrady66:dLpyb10SKl8FHRNX@pennapps.wzkt4.mongodb.net/?retryWrites=true&w=majority&tls=true&tlsAllowInvalidCertificates=false')

    db = client['health_data_db']  # Database name
    collection = db['health_records']  # Collection name

    # Insert cleaned data into MongoDB
    if data:
        collection.insert_many(data)
        print(f"Inserted {len(data)} records into MongoDB.")
    else:
        print("No data to insert.")

if __name__ == "__main__":
    # File path to your Apple Health export file
    file_path = "/Users/alexdang/Desktop/HackingPennapps/apple_health_export/export.xml"
    
    # Clean the data
    cleaned_output = clean_health_data(file_path)
    
    # Push the cleaned data to MongoDB
    push_to_mongo(cleaned_output)
