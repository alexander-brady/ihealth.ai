import os
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient

app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = '/Users/alexdang/ihealth.ai/uploads'
OUTPUT_FOLDER = '/Users/alexdang/ihealth.ai/cool'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

MONGO_URI = ""
# Initialize MongoDB client
client = MongoClient(MONGO_URI)
db = client['health_data']  # Name of your database
collection = db['combined_health_metrics_Pokemon']  # Name of your collection
# Function to clean heart rate data
# Function to clean heart rate data (also applicable for other data types)
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

            # Check if the record has a valid 'endDate'
            if end_date is None:
                print(f"Warning: Missing 'endDate' for record of type {record_type}")
                continue  # Skip this record

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


# Function to clean data by date range (handles missing endDate)
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

            # Skip records without startDate or endDate
            if not start_date or not end_date:
                print(f"Warning: Missing 'startDate' or 'endDate' for record type {record_type}")
                continue

            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S %z").replace(tzinfo=None)
            end_date_dt = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S %z").replace(tzinfo=None)

            # Check for records within date range
            if start_filter_date <= start_date_dt <= end_filter_date:
                cleaned_data.append({
                    'type': record_type,
                    'value': record_value,
                    'startDate': start_date_dt,
                    'endDate': end_date_dt,
                })

        return cleaned_data

    except Exception as e:
        print(f"Error processing XML (By Date): {str(e)}")
        return None


# Function to clean and update sleep data with sequential dates
def clean_sleep_analysis_data(file_path, start_date_str, end_date_str):
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()

        start_filter_date = datetime.strptime(start_date_str, "%Y-%m-%d")
        end_filter_date = datetime.strptime(end_date_str, "%Y-%m-%d")

        cleaned_data = []
        for record in root.findall('Record'):
            record_type = record.get('type')
            
            # Only process sleep analysis records
            if record_type != "HKCategoryTypeIdentifierSleepAnalysis":
                continue

            start_date = record.get('startDate')
            end_date = record.get('endDate')

            # Skip records without startDate or endDate
            if not start_date or not end_date:
                print(f"Warning: Missing 'startDate' or 'endDate' for record type {record_type}")
                continue

            # Convert the startDate and endDate to datetime objects
            start_date_dt = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S %z").replace(tzinfo=None)
            end_date_dt = datetime.strptime(end_date, "%Y-%m-%d %H:%M:%S %z").replace(tzinfo=None)

            # Filter records within the specified date range
            if start_filter_date <= start_date_dt <= end_filter_date:
                sleep_duration = (end_date_dt - start_date_dt).total_seconds() / 3600  # in hours

                # Append the cleaned data for sleep analysis records
                cleaned_data.append({
                    'type': record_type,
                    'startDate': start_date_dt,
                    'endDate': end_date_dt,
                    'sleepDurationHours': sleep_duration
                })

        return cleaned_data

    except Exception as e:
        print(f"Error processing XML (Sleep): {str(e)}")
        return None


# Sequentially update sleep analysis dates
def update_sleep_analysis_dates_sequentially(data, new_start_date_str):
    new_start_date = datetime.strptime(new_start_date_str, "%Y-%m-%d")
    time_deltas = data['endDate'] - data['startDate']

    new_start_dates = [new_start_date]
    new_end_dates = [new_start_date + time_deltas.iloc[0]]

    for i in range(1, len(data)):
        new_start_dates.append(new_end_dates[-1] + timedelta(seconds=1))
        if new_start_dates[-1].date() == new_start_dates[-2].date():
            new_start_dates[-1] += timedelta(days=1)
        new_end_dates.append(new_start_dates[-1] + time_deltas.iloc[i])

    data['startDate'] = new_start_dates
    data['endDate'] = new_end_dates
    return data
@app.route('/fetch-heart-rate', methods=['GET'])
def fetch_heart_rate():
    try:
        # Fetch heart rate data from MongoDB
        heart_rate_data = collection.find({"type": "HKQuantityTypeIdentifierHeartRate"})
        heart_rate_list = []
        
        # Loop through the data and prepare it for the frontend
        for record in heart_rate_data:
            heart_rate_list.append({
                "value": record.get("value"),
                "startDate": record.get("startDate"),
                "endDate": record.get("endDate")
            })

        # Return the data as JSON
        return jsonify({"heart_rate_data": heart_rate_list}), 200

    except Exception as e:
        print(f"Error fetching data: {str(e)}")
        return jsonify({"error": f"Failed to fetch data: {str(e)}"}), 500

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
            end_date_str_heart_rate = "2024-09-19"
            cleaned_heart_rate_data = clean_heart_rate_data(file_path, start_date_str_heart_rate, end_date_str_heart_rate)

            if cleaned_heart_rate_data is None:
                return jsonify({"error": "Error processing heart rate data."}), 500

            df_heart_rate = pd.DataFrame(cleaned_heart_rate_data)
            output_csv_heart_rate = os.path.join(UPLOAD_FOLDER, 'cleaned_heart_rate_data.csv')
            if not df_heart_rate.empty:
                df_heart_rate.to_csv(output_csv_heart_rate, index=False)
            else:
                return jsonify({"error": "No heart rate records found for the date range."}), 400

            # 2. Clean non-sleep data by date
            start_date_str_data_by_date = "2024-08-23"
            end_date_str_data_by_date = "2024-09-19"
            cleaned_data_by_date = clean_data_by_date(file_path, start_date_str_data_by_date, end_date_str_data_by_date)

            if cleaned_data_by_date is None:
                return jsonify({"error": "Error processing non-sleep data."}), 500

            df_data_by_date = pd.DataFrame(cleaned_data_by_date)
            output_csv_data_by_date = os.path.join(UPLOAD_FOLDER, 'cleaned_data_by_date.csv')
            if not df_data_by_date.empty:
                df_data_by_date.to_csv(output_csv_data_by_date, index=False)
            else:
                return jsonify({"error": "No non-sleep records found for the date range."}), 400

            # 3. Process and update sleep analysis data
            start_date_str_sleep = "2020-01-07"
            end_date_str_sleep = "2020-03-12"
            new_start_date_sleep = "2024-08-23"
            cleaned_sleep_data = clean_sleep_analysis_data(file_path, start_date_str_sleep, end_date_str_sleep)

            if cleaned_sleep_data is None:
                return jsonify({"error": "Error processing sleep data."}), 500

            df_sleep = pd.DataFrame(cleaned_sleep_data)
            updated_df_sleep = update_sleep_analysis_dates_sequentially(df_sleep, new_start_date_sleep)
            output_csv_sleep = os.path.join(UPLOAD_FOLDER, 'updated_sleep_analysis_data.csv')
            updated_df_sleep.to_csv(output_csv_sleep, index=False)

            # 4. Combine heart rate, non-sleep, and sleep data
            combined_csv_output = os.path.join(OUTPUT_FOLDER, 'combined_updated_health_data.csv')

            # Read the CSV files
            heart_rate_df = pd.read_csv(output_csv_heart_rate)
            non_sleep_df = pd.read_csv(output_csv_data_by_date)
            sleep_df = pd.read_csv(output_csv_sleep)

            # Combine them
            combined_df = pd.concat([heart_rate_df, non_sleep_df, sleep_df], ignore_index=True)

            # Save the combined data
            combined_df.to_csv(combined_csv_output, index=False)
            
            # 5. Upload combined data to MongoDB
            combined_data = combined_df.to_dict(orient='records')  # Convert the combined dataframe to a list of dictionaries
            collection.insert_many(combined_data)  # Insert the combined data into MongoDB collection
            inserted_count = len(combined_data)
            print(f"Successfully inserted {inserted_count} records into MongoDB")

            return jsonify({
                "message": "All data processed and combined successfully",
                "csv_heart_rate": output_csv_heart_rate,
                "csv_data_by_date": output_csv_data_by_date,
                "csv_sleep_data": output_csv_sleep,
                "csv_combined": combined_csv_output
            }), 200

        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify({"error": f"File processing failed: {str(e)}"}), 500
    else:
        return jsonify({"error": "No file received"}), 400

if __name__ == '__main__':
    app.run(debug=True)
