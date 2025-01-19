import os
import google.generativeai as genai
import re
from datetime import datetime
from google.cloud import translate_v2
from flask import Flask, request, jsonify

app = Flask(__name__)

def setup_gemini():
    """Configure Gemini API with the provided key"""
    genai.configure(api_key="AIzaSyC7-YhQoMLVhx2J_S_U_bnp917sqoEZ-JI")

    generation_config = {
        "temperature": 0.7,
        "top_p": 0.95,
        "top_k": 40,
        "max_output_tokens": 2048,
    }

    return genai.GenerativeModel(
        model_name="gemini-1.0-pro",
        generation_config=generation_config,
    )

def setup_translation_client():
    """Set up Google Translate API client"""
    return translate_v2.Client.from_service_account_json("gen-lang-client-0182388257-027b6c8204af.json")

def clean_response(response_text):
    """Clean the response to remove unnecessary text"""
    cleaned = re.sub(r'\[.*?\]', '', response_text)  # Remove square bracket content
    cleaned = cleaned.split("Suggested responses")[0] if "Suggested responses" in cleaned else cleaned
    cleaned = re.sub(r'Shopkeeper:?', '', cleaned)  # Remove 'Shopkeeper:' text
    return " ".join(cleaned.split()).strip()  # Clean up whitespace

def get_greeting():
    """Generate a greeting based on the time of day."""
    hour = datetime.now().hour
    if hour < 12:
        return "Good morning!"
    elif 12 <= hour < 18:
        return "Good afternoon!"
    else:
        return "Good evening!"

def translateText(client, text, target_language):
    """Translate the given text to the target language"""
    result = client.translate_v2(text, target_language=target_language)
    return result["translatedText"]

def handle_clarification(user_input):
    """Provide clarifications for unclear input."""
    clarifications = [
        "I didn’t quite catch that. Are you asking about a specific item or price?",
        "Could you rephrase or provide more details?",
        "I’m here to help! Can you let me know what you’re looking for?"
    ]
    return clarifications[hash(user_input) % len(clarifications)]

@app.route('/generate-story', methods=['POST'])
def generate_story():
    """Handle the grocery conversation API endpoint."""
    try:
        # Get input data from the request
        data = request.json
        user_input = data.get('user_input')
        preferred_language = data.get('preferred_language', 'en')

        if not user_input:
            return jsonify({"error": "User input is required"}), 400

        model = setup_gemini()
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
        user_input_translated = translate_text(translation_client, user_input, 'en')

        # Get response from Gemini model
        response = chat.send_message(f"Customer: {user_input_translated}\nRespond naturally without showing instructions or context.")
        if response and hasattr(response, 'text'):
            cleaned_response = clean_response(response.text)

            if not cleaned_response or "I didn't quite understand" in cleaned_response:
                clarification = handle_clarification(user_input)
                translated_clarification = translate_text(translation_client, clarification, preferred_language)
                return jsonify({"response": translated_clarification, "english_response": clarification})
            else:
                translated_response = translate_text(translation_client, cleaned_response, preferred_language)
                return jsonify({"response": translated_response, "english_response": cleaned_response})

        else:
            clarification = handle_clarification(user_input)
            translated_clarification = translate_text(translation_client, clarification, preferred_language)
            return jsonify({"response": translated_clarification, "english_response": clarification})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
