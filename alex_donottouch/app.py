import os
import xml.etree.ElementTree as ET
from datetime import datetime
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = '/Users/alexdang/ihealth.ai/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Function to clean heart rate data
def clean_heart_rate_data(file_path, start_date_str, end_date_str):
    try:
        tree = ET.parse(file_path)  # Parse the file
        root = tree.getroot()

        start_filter_date = datetime.strptime(start_date_str, "%Y-%m-%d").date()
        end_filter_date = datetime.strptime(end_date_str, "%Y-%m-%d").date()

        cleaned_data = []
        for record in root.findall('Record'):
            record_type = record.get('type')
            record_value = record.get('value')
            start_date = record.get('startDate')
            end_date = record.get('endDate')

            # Convert dates
            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S %z")
            end_date_dt = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S %z")

            # Debug: Log what is being processed
            print(f"Record Type: {record_type}, Start Date: {start_date}, Value: {record_value}")

            # Check for heart rate records within date range
            if record_type == "HKQuantityTypeIdentifierHeartRate" and start_filter_date <= start_date_dt.date() <= end_filter_date:
                cleaned_data.append({
                    'type': record_type,
                    'value': record_value,
                    'startDate': start_date_dt,
                    'endDate': end_date_dt,
                })

        return cleaned_data

    except Exception as e:
        print(f"Error processing XML: {str(e)}")
        return None

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file:
        try:
            # Save uploaded XML file
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            print(f"File saved successfully at: {file_path}")  # Debug: Confirm file saved

            # Clean heart rate data after upload
            start_date_str = "2024-09-19"
            end_date_str = "2024-09-20"

            cleaned_heart_rate_data = clean_heart_rate_data(file_path, start_date_str, end_date_str)

            if cleaned_heart_rate_data is None:
                return jsonify({"error": "Error processing the uploaded XML file."}), 500

            # Convert to Pandas DataFrame
            df = pd.DataFrame(cleaned_heart_rate_data)

            print(f"DataFrame created with {len(df)} rows.")  # Debug: Check DataFrame size

            # Save the cleaned data to a CSV file
            output_csv_path = os.path.join(UPLOAD_FOLDER, 'cleaned_heart_rate_data.csv')
            if not df.empty:
                df.to_csv(output_csv_path, index=False)
                print(f"Heart rate data successfully saved to {output_csv_path}")  # Debug: Confirm CSV saved
                return jsonify({"message": "File processed and CSV saved successfully", "csv_path": output_csv_path}), 200
            else:
                print("No heart rate records found for the specified date range.")  # Debug: No data
                return jsonify({"error": "No heart rate records found for the specified date range"}), 400

        except Exception as e:
            print(f"Error: {str(e)}")  # Print error in console for debugging
            return jsonify({"error": f"File processing failed: {str(e)}"}), 500
    else:
        print("No file received")  # Debugging output to ensure this case is caught
        return jsonify({"error": "No file received"}), 400

if __name__ == '__main__':
    app.run(debug=True)
