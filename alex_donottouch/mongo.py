from flask import Flask, jsonify
from pymongo import MongoClient
import numpy as np

app = Flask(__name__)

# Initialize MongoDB client
MONGO_URI = "mongodb+srv://alexjbrady66:dLpyb10SKl8FHRNX@pennapps.wzkt4.mongodb.net/?retryWrites=true&w=majority&appName=PennApps"
client = MongoClient(MONGO_URI)
db = client['health_data']
heart_rate_collection = db['combined_health_metrics_Pokemon']
sleep_analysis_collection = db['combined_health_metrics_Pokemon']

# Helper function for heart rate analysis
def analyze_heart_rate():
    heart_rate_data = list(heart_rate_collection.find({"type": "HKQuantityTypeIdentifierHeartRate"}))
    heart_rates = [float(record['value']) for record in heart_rate_data]

    if not heart_rates:
        return None, None, None, 0, 0, "No heart rate data available."

    avg_heart_rate = np.mean(heart_rates)
    min_heart_rate = np.min(heart_rates)
    max_heart_rate = np.max(heart_rates)

    # Define thresholds for bradycardia and tachycardia
    bradycardia_count = sum(1 for hr in heart_rates if hr < 60)
    tachycardia_count = sum(1 for hr in heart_rates if hr > 100)

    if bradycardia_count > 0:
        comment = "Bradycardia detected."
    elif tachycardia_count > 0:
        comment = "Tachycardia detected."
    else:
        comment = "Heart rate is within a normal range."

    return avg_heart_rate, min_heart_rate, max_heart_rate, bradycardia_count, tachycardia_count, comment

# Helper function for sleep analysis
def analyze_sleep():
    sleep_data = list(sleep_analysis_collection.find({"type": "HKCategoryTypeIdentifierSleepAnalysis"}))
    sleep_durations = [float(record['sleepDurationHours']) for record in sleep_data]

    if not sleep_durations:
        return None, None, None, 0, 0, 0, "No sleep data available."

    avg_sleep_duration = np.mean(sleep_durations)
    min_sleep_duration = np.min(sleep_durations)
    max_sleep_duration = np.max(sleep_durations)

    # Define thresholds for sleep duration
    too_little_count = sum(1 for sd in sleep_durations if sd < 6)
    normal_count = sum(1 for sd in sleep_durations if 6 <= sd <= 9)
    too_much_count = sum(1 for sd in sleep_durations if sd > 9)

    if too_little_count > 0:
        comment = "You are getting too little sleep."
    elif too_much_count > 0:
        comment = "You are getting too much sleep."
    else:
        comment = "Your sleep duration is within a healthy range."

    return avg_sleep_duration, min_sleep_duration, max_sleep_duration, too_little_count, normal_count, too_much_count, comment

# Function to generate combined analysis for LLM input
@app.route('/analyze-health', methods=['GET'])
def analyze_health():
    # Analyze heart rate data
    avg_heart_rate, min_heart_rate, max_heart_rate, bradycardia_count, tachycardia_count, hr_comment = analyze_heart_rate()
    
    # Analyze sleep data
    avg_sleep_duration, min_sleep_duration, max_sleep_duration, too_little_count, normal_count, too_much_count, sleep_comment = analyze_sleep()

    # Combine results into a structured summary
    analysis_summary = {
        "heart_rate": {
            "average_heart_rate": avg_heart_rate,
            "min_heart_rate": min_heart_rate,
            "max_heart_rate": max_heart_rate,
            "bradycardia_count": bradycardia_count,
            "tachycardia_count": tachycardia_count,
            "comment": hr_comment,
        },
        "sleep_analysis": {
            "average_sleep_duration": avg_sleep_duration,
            "min_sleep_duration": min_sleep_duration,
            "max_sleep_duration": max_sleep_duration,
            "too_little_sleep_count": too_little_count,
            "normal_sleep_count": normal_count,
            "too_much_sleep_count": too_much_count,
            "comment": sleep_comment,
        },
        "combined_comment": f"Heart Rate Analysis: {hr_comment}. Sleep Analysis: {sleep_comment}."
    }

    return jsonify(analysis_summary), 200

if __name__ == '__main__':
    app.run(debug=True)
