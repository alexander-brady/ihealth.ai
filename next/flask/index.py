import os
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
from openai import OpenAI
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.llms.base import LLM
from langchain.chains import ConversationChain
from pydantic import BaseModel, Field
from typing import Optional, List
from pymongo import MongoClient
import numpy as np
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import pandas as pd
# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Set OpenAI API key from environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY environment variable not found.")

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# Custom LLM Class with OpenAI client and streaming
class OpenAILLM(LLM, BaseModel):
    model_name: str = Field(default="gpt-3.5-turbo")

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        try:
            response = client.chat.completions.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                stream=True
            )
            # Collect the response chunks and join them together
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
            return full_response
        except Exception as e:
            raise RuntimeError(f"Failed to generate response: {str(e)}")

    @property
    def _identifying_params(self):
        return {"model_name": self.model_name}

    @property
    def _llm_type(self) -> str:
        return "openai"

UPLOAD_FOLDER = '/Users/alexdang/ihealth.ai/uploads'
OUTPUT_FOLDER = '/Users/alexdang/ihealth.ai/cool'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

MONGO_URI = "mongodb+srv://alexjbrady66:dLpyb10SKl8FHRNX@pennapps.wzkt4.mongodb.net/?retryWrites=true&w=majority&appName=PennApps"
if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable not found.")

mongo_client = MongoClient(MONGO_URI)
db = mongo_client['health_data']  # Name of your MongoDB database
collection = db['combined_health_metrics_Pokemon']  # Name of your collection

# Initialize Conversation Memory
memory = ConversationBufferMemory()

# Create a PromptTemplate
prompt_template = PromptTemplate(
    input_variables=["input"],
    template="The user said: {input}"
)

# Create a ConversationChain with the custom LLM and memory
llm = OpenAILLM(model_name="gpt-3.5-turbo")
conversation_chain = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)



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
# Initialize the model with the initial health prompt
#line below necessary anymore?
# memory.save_context({"system": "Healthcare Assistant"}, {"message": initial_prompt})

isInitialPrompt = True



@app.route('/send-message', methods=['POST'])
def send_message():
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

        return analysis_summary


    global isInitialPrompt
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    try:
        # Use ConversationChain to process input and generate response with conversation history
        if isInitialPrompt:
            isInitialPrompt = False
            db = mongo_client['health_data']
            heart_rate_collection = db['combined_health_metrics_Pokemon']
            sleep_analysis_collection = db['combined_health_metrics_Pokemon']
            # print(heart_rate_collection)
            # print(sleep_analysis_collection)

            health_data = analyze_health()
            print(health_data)

            # Initial prompt for health-related questions
            #we won't have health_data right away in most cases! need to fix this
            initial_prompt = (
                f"""You are a healthcare assistant. Your task is to ask health-related questions
                to determine if the user needs to see a doctor. Start the conversation by asking the user about their health.
                make it so that if you have enough information to determine whether they need to see the doctor or not, if the need to see it say: You should go see a doctor. And then give a description of why they should.
                if they do not need to see a doctor. You should not see a doctor. And explain why they shouldn't.
                also, base your questions primarily off of anomalies or problems in the apple watch data fetched for the user below:
                {health_data}
                """
            )
            memory.save_context({"system": "Healthcare Assistant"}, {"message": initial_prompt})

            result = conversation_chain.run({"input": user_message})

            # Return the AI response with conversation history
            return jsonify({'text': result, 'history': memory.buffer})
        else:
            result = conversation_chain.run({"input": user_message})

            # Return the AI response with conversation history
            return jsonify({'text': result, 'history': memory.buffer})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/send-message-stream', methods=['POST'])
def send_message_stream():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    def generate_response_stream(message):
        try:
            # Use streaming feature for OpenAI LLM
            response = client.chat.completions.create(
                model=llm.model_name,
                messages=[{"role": "user", "content": message}],
                stream=True
            )
            # Stream the response chunks back
            for chunk in response:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            yield f"Error: {str(e)}"

    # Return streamed response as text/event-stream
    return Response(generate_response_stream(user_message), content_type='text/event-stream')

@app.route('/clear-history', methods=['POST'])
def clear_history():
    """Endpoint to clear chat history."""
    global memory
    memory.clear()
    return jsonify({'message': 'Chat history cleared.'})

if __name__ == '__main__':
    app.run(debug=True)
