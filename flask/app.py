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

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI environment variable not found.")

mongo_client = MongoClient(MONGO_URI)
db = mongo_client['health_data']

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

heart_rate_collection = db['combined_health_metrics_Pokemon']
sleep_analysis_collection = db['combined_health_metrics_Pokemon']
# print(heart_rate_collection)
# print(sleep_analysis_collection)

health_data = analyze_health()
print(health_data)

# Initial prompt for health-related questions
initial_prompt = (
    f"""You are a healthcare assistant. Your task is to ask health-related questions
    to determine if the user needs to see a doctor. Start the conversation by asking the user about their health.
    make it so that if you have enough information to determine whether they need to see the doctor or not, if the need to see it say: You should go see a doctor. And then give a description of why they should.
    if they do not need to see a doctor. You should not see a doctor. And explain why they shouldn't.
    also, base your questions primarily off of anomalies or problems in the apple watch data fetched for the user below:
    {health_data}
    """
)

# Initialize the model with the initial health prompt
memory.save_context({"system": "Healthcare Assistant"}, {"message": initial_prompt})

@app.route('/send-message', methods=['POST'])
def send_message():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'Message is required'}), 400

    try:
        # Use ConversationChain to process input and generate response with conversation history
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
