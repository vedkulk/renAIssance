from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests
import re
import pyttsx3
import google.generativeai as genai
from datetime import datetime
from google.cloud import translate_v2 as google_translate

# Load environment variables
load_dotenv()

WORQHAT_API_KEY = os.getenv("WORQHAT_API_KEY")

app = Flask(__name__)

# Enable CORS for the entire app
CORS(app, origins=["http://localhost:5173"], methods=["GET", "POST", "OPTIONS"], supports_credentials=True)

os.environ["GEMINI_API_KEY"] = "AIzaSyAHqnVJz1wt68y4gavOVqtQmHbFcVVK194"  
genai.configure(api_key=os.environ["GEMINI_API_KEY"])

# Initialize the generative model (only once for the whole app)
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        generation_config=generation_config,
    )
except Exception as e:
    print("Error initializing generative model:", str(e))
    model = None

def setup_translation_client():
    """Set up Google Translate API client"""
    return google_translate.Client.from_service_account_json("gen-lang-client-0182388257-027b6c8204af.json")

def translateText(client, text, target_language):
    """Translate the given text to the target language"""
    result = client.translate(text, target_language=target_language)  # Correct method
    return result["translatedText"]

def clean_response(response_text):
    """Clean the response to remove unnecessary text"""
    cleaned = re.sub(r'\[.*?\]', '', response_text)  # Remove square bracket content
    cleaned = cleaned.split("Suggested responses")[0] if "Suggested responses" in cleaned else cleaned
    cleaned = re.sub(r'Shopkeeper:?', '', cleaned)  # Remove 'Shopkeeper:' text
    return " ".join(cleaned.split()).strip()  # Clean up whitespace

def handle_clarification(user_input):
    """Provide clarifications for unclear input."""
    clarifications = [
        "I didn’t quite catch that. Are you asking about a specific item or price?",
        "Could you rephrase or provide more details?",
        "I’m here to help! Can you let me know what you’re looking for?"
    ]
    return clarifications[hash(user_input) % len(clarifications)]

def get_greeting():
    """Generate a greeting based on the time of day."""
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning!"
    elif 12 <= hour < 18:
        return "Good afternoon!"
    else:
        return "Good evening!"

@app.route("/generate-story", methods=["POST"])
def generate_story():
    """Endpoint to generate a story based on language and difficulty."""
    try:
        data = request.json
        print("Request received:", data)  # Log the incoming request

        language = data.get("language")
        difficulty = data.get("difficulty")

        # Validate request data
        if not language or not difficulty:
            error_message = "Language and difficulty are required."
            print("Error:", error_message)
            return jsonify({"error": error_message}), 400

        # Create the prompt based on difficulty
        if difficulty == "Easy":
            prompt = (
                f"Generate a short story in English. Include simple sentences in {language} such as greetings or exclamatory reactions."
            )
        elif difficulty == "Moderate":
            prompt = (
                f"Generate a short story in English. Include dialogues in {language}, and translate each dialogue into English within parentheses."
            )
        else:  # High difficulty
            prompt = (
                f"Generate a short story with most sentences in {language} and some in English. Translate non-English sentences into English within parentheses."
            )

        print("Generated prompt:", prompt)  # Log the generated prompt

        # Ensure the model is initialized
        if model is None:
            error_message = "Generative model not initialized. Check your API configuration."
            print("Error:", error_message)
            return jsonify({"error": error_message}), 500

        # Send the prompt to the API
        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(prompt)

        print("API response:", response.text)  # Log the API response
        return jsonify({"story": response.text})

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        print(error_message)  # Log the error
        return jsonify({"error": error_message}), 500

@app.route('/grocery-conversation', methods=['POST'])
def grocery_conversation():
    """Handle the grocery conversation API endpoint."""
    try:
        # Get input data from the request
        data = request.json
        user_input = data.get('user_input')
        preferred_language = data.get('preferred_language', 'en')

        if not user_input:
            return jsonify({"error": "User input is required"}), 400

        # Initialize translation client
        translation_client = setup_translation_client()

        # Define the context for the conversation
        context = """You are a friendly and knowledgeable grocery store shopkeeper. 
        Help customers with their queries, suggest related items, and ensure they have a pleasant experience. 
        Here's your inventory with prices:
        
        - Fresh Tomatoes ($2.99/lb)
        - Lettuce ($2.49/head)
        - Carrots ($1.99/lb)
        - Cucumbers ($1.49 each)
        - Apples ($1.99/lb)
        - Bananas ($0.59/lb)
        - Oranges ($2.49/lb)
        - Fresh Herbs ($1.99/bunch)

        Suggest related items when appropriate. Keep your tone friendly and conversational."""

        # Start chat and initialize with context
        chat = model.start_chat(history=[])
        chat.send_message(context)

        # Translate user input to English if necessary
        user_input_translated = translateText(translation_client, user_input, 'en')

        # Get response from Gemini model
        response = chat.send_message(f"Customer: {user_input_translated}\nRespond naturally without showing instructions or context.")
        if response and hasattr(response, 'text'):
            cleaned_response = clean_response(response.text)

            if not cleaned_response or "I didn't quite understand" in cleaned_response:
                clarification = handle_clarification(user_input)
                translated_clarification = translateText(translation_client, clarification, preferred_language)
                return jsonify({"response": translated_clarification, "english_response": clarification})
            else:
                translated_response = translateText(translation_client, cleaned_response, preferred_language)
                return jsonify({"response": translated_response, "english_response": cleaned_response})

        else:
            clarification = handle_clarification(user_input)
            translated_clarification = translateText(translation_client, clarification, preferred_language)
            return jsonify({"response": translated_clarification, "english_response": clarification})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def translate_text(input_text, target_language, model_name="aicon-v4-nano-160824"):
    """
    Translate input text to the target language using WorqHat's API.
    """
    try:
        response = requests.post(
            "https://api.worqhat.com/api/ai/content/v4",
            headers={"Authorization": f"Bearer {WORQHAT_API_KEY}"},
            json={
                "question": f"Translate this text to {target_language}: {input_text}",
                "model": model_name,
            },
        )
        response_data = response.json()
        if response.status_code == 200:
            return response_data.get("content", "Translation not available.")
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"An exception occurred: {e}"

@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    input_text = data.get('input_text')
    target_language = data.get('target_language')
    
    if not input_text or not target_language:
        return jsonify({"error": "Missing input text or target language"}), 400
    
    translated_text = translate_text(input_text, target_language)
    
    return jsonify({"translated_text": translated_text})

@app.route('/speak', methods=['POST'])
def speak():
    """Text-to-Speech endpoint."""
    data = request.get_json()
    text_to_speak = data.get('text')

    if not text_to_speak:
        return jsonify({"error": "Missing text to speak"}), 400

    # Initialize the TTS engine
    engine = pyttsx3.init()

    # Speak the text
    engine.say(text_to_speak)
    engine.runAndWait()

    return jsonify({"message": "Text has been spoken."})

if __name__ == "__main__":
    app.run(debug=True)
