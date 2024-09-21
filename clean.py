import xml.etree.ElementTree as ET

def clean_health_data(file_path):
    # Parse the XML from the file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Extract relevant fields for both sleep analysis and walking/running distance
    cleaned_data = []
    for record in root.findall('Record'):
        record_type = record.get('type')
        record_value = record.get('value')
        start_date = record.get('startDate')
        end_date = record.get('endDate')
        
        # Process 'HKCategoryTypeIdentifierSleepAnalysis' and 'HKQuantityTypeIdentifierDistanceWalkingRunning' records
        if record_type == "HKCategoryTypeIdentifierSleepAnalysis" or record_type == "HKQuantityTypeIdentifierDistanceWalkingRunning" or record_type == "HKQuantityTypeIdentifierStepCount":
            cleaned_data.append({
                'type': record_type,
                'value': record_value,
                'startDate': start_date,
                'endDate': end_date
            })

    return cleaned_data

if __name__ == "__main__":
    # File path to your Apple Health export file
    file_path = "/Users/alexdang/Desktop/HackingPennapps/apple_health_export/export.xml"
    
    # Clean the data
    cleaned_output = clean_health_data(file_path)
    
    # Print the cleaned output
    for record in cleaned_output:
        print(record)
