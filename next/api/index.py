import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from cerebras.cloud.sdk import Cerebras
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.llms.base import LLM
from langchain.chains import ConversationChain
from pydantic import BaseModel, Field
from typing import Optional, List

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Create Cerebras client using API key from environment variables
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")
if not CEREBRAS_API_KEY:
    raise ValueError("CEREBRAS_API_KEY environment variable not found.")

cerebras_client = Cerebras(api_key=CEREBRAS_API_KEY)

# Custom LLM Class with Cerebras client
class CerebrasLLM(LLM, BaseModel):
    client: Cerebras = Field(...)
    model_name: str = Field(default="llama3.1-8b")

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model_name
            )
            return response.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Failed to generate response: {str(e)}")

    @property
    def _identifying_params(self):
        return {"model_name": self.model_name}

    @property
    def _llm_type(self) -> str:
        return "cerebras"

# Initialize Conversation Memory
memory = ConversationBufferMemory()

# Initial prompt for health-related questions
initial_prompt = (
    '''You are a healthcare assistant. Your task is to ask health-related questions
    to determine if the user needs to see a doctor. Start the conversation by asking the user about their health.
    make it so that if you have enough information to determine whether they need to see the doctor or not, if the need to see it say: You should go see a doctor. And then give a description of why they should.
    if they do not need to see a doctor. You should not see a doctor. And explain why they shouldn't.'''
)

# Create a PromptTemplate
prompt_template = PromptTemplate(
    input_variables=["input"],
    template="The user said: {input}"
)

# Create a ConversationChain with the custom LLM and memory
llm = CerebrasLLM(client=cerebras_client, model_name="llama3.1-8b")
conversation_chain = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
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

@app.route('/clear-history', methods=['POST'])
def clear_history():
    """Endpoint to clear chat history."""
    global memory
    memory.clear()
    return jsonify({'message': 'Chat history cleared.'})

if __name__ == '__main__':
    app.run(debug=True)