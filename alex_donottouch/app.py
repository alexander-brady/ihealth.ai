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
        print(f"Error processing XML (Heart Rate): {str(e)}")
        return None

# Function to clean data by date range
def clean_data_by_date(file_path, start_date_str, end_date_str):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        start_filter_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_filter_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        cleaned_data = []
        for record in root.findall('Record'):
            record_type = record.get('type')
            record_value = record.get('value')
            start_date = record.get('startDate')
            end_date = record.get('endDate')

            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S %z").replace(tzinfo=None)
            end_date_dt = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S %z").replace(tzinfo=None)

            # Check for records within date range
            if start_filter_date <= start_date_dt <= end_filter_date:
                cleaned_data.append({
                    'type': record_type,
                    'value': record_value,
                    'startDate': start_date,
                    'endDate': end_date,
                })

        return cleaned_data

    except Exception as e:
        print(f"Error processing XML (By Date): {str(e)}")
        return None

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files.get('file')
    if file:
        try:
            # Save uploaded XML file
            file_path = os.path.join(UPLOAD_FOLDER, file.filename)
            file.save(file_path)

            print(f"File saved successfully at: {file_path}")

            # 1. Clean heart rate data
            start_date_str_heart_rate = "2024-09-19"
            end_date_str_heart_rate = "2024-09-20"

            cleaned_heart_rate_data = clean_heart_rate_data(file_path, start_date_str_heart_rate, end_date_str_heart_rate)

            if cleaned_heart_rate_data is None:
                return jsonify({"error": "Error processing the uploaded XML file (Heart Rate)."}), 500

            df_heart_rate = pd.DataFrame(cleaned_heart_rate_data)

            output_csv_heart_rate = os.path.join(UPLOAD_FOLDER, 'cleaned_heart_rate_data.csv')
            if not df_heart_rate.empty:
                df_heart_rate.to_csv(output_csv_heart_rate, index=False)
                print(f"Heart rate data successfully saved to {output_csv_heart_rate}")
            else:
                return jsonify({"error": "No heart rate records found for the specified date range"}), 400

            # 2. Clean data by date
            start_date_str_data_by_date = "2024-08-23"
            end_date_str_data_by_date = "2024-09-19"

            cleaned_data_by_date = clean_data_by_date(file_path, start_date_str_data_by_date, end_date_str_data_by_date)

            if cleaned_data_by_date is None:
                return jsonify({"error": "Error processing the uploaded XML file (By Date)."}), 500

            df_data_by_date = pd.DataFrame(cleaned_data_by_date)

            output_csv_data_by_date = os.path.join(UPLOAD_FOLDER, 'cleaned_data_by_date.csv')
            if not df_data_by_date.empty:
                df_data_by_date.to_csv(output_csv_data_by_date, index=False)
                print(f"Data by date successfully saved to {output_csv_data_by_date}")
            else:
                return jsonify({"error": "No records found within the specified date range"}), 400

            return jsonify({
                "message": "Both files processed successfully",
                "csv_heart_rate": output_csv_heart_rate,
                "csv_data_by_date": output_csv_data_by_date
            }), 200

        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify({"error": f"File processing failed: {str(e)}"}), 500
    else:
        return jsonify({"error": "No file received"}), 400

if __name__ == '__main__':
    app.run(debug=True)
