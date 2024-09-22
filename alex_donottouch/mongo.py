from flask import Flask, jsonify
from pymongo import MongoClient
import numpy as np

app = Flask(__name__)

# Initialize MongoDB client
MONGO_URI = "mongodb+srv://<your_uri>"
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

# Helper function for walking/running distance analysis
def analyze_walking_running_distance():
    distance_data = list(heart_rate_collection.find({"type": "HKQuantityTypeIdentifierDistanceWalkingRunning"}))
    distances = [float(record['value']) for record in distance_data]

    if not distances:
        return None, None, None, "No distance walking/running data available."

    avg_distance = np.mean(distances)
    min_distance = np.min(distances)
    max_distance = np.max(distances)

    too_little_distance_count = sum(1 for dist in distances if dist < 0.5)  # Example: consider distances below 0.5 km as low
    moderate_distance_count = sum(1 for dist in distances if 0.5 <= dist <= 2)
    long_distance_count = sum(1 for dist in distances if dist > 2)

    if too_little_distance_count > 0:
        comment = "You are walking/running very short distances. Consider increasing your activity for better health."
    elif long_distance_count > 0:
        comment = "Great job! You are walking/running long distances, which is excellent for your health."
    else:
        comment = "Your walking/running distance is in a moderate range."

    return avg_distance, min_distance, max_distance, too_little_distance_count, moderate_distance_count, long_distance_count, comment

# Function to generate combined health analysis
def generate_health_analysis():
    # Analyze heart rate data
    avg_heart_rate, min_heart_rate, max_heart_rate, bradycardia_count, tachycardia_count, hr_comment = analyze_heart_rate()
    
    # Analyze sleep data
    avg_sleep_duration, min_sleep_duration, max_sleep_duration, too_little_count, normal_count, too_much_count, sleep_comment = analyze_sleep()

    # Analyze walking/running distance data
    avg_distance, min_distance, max_distance, too_little_distance_count, moderate_distance_count, long_distance_count, distance_comment = analyze_walking_running_distance()

    # Combine results into a structured summary
    health_analysis = {
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
        "walking_running_distance": {
            "average_distance": avg_distance,
            "min_distance": min_distance,
            "max_distance": max_distance,
            "too_little_distance_count": too_little_distance_count,
            "moderate_distance_count": moderate_distance_count,
            "long_distance_count": long_distance_count,
            "comment": distance_comment,
        },
        "combined_comment": f"Heart Rate Analysis: {hr_comment}. Sleep Analysis: {sleep_comment}. Distance Analysis: {distance_comment}."
    }

    return health_analysis
