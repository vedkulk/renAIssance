from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import requests
import pyttsx3

# Load environment variables
load_dotenv()

WORQHAT_API_KEY = os.getenv("WORQHAT_API_KEY")

app = Flask(__name__)

# Enable CORS for the entire app
CORS(app, origins=["http://localhost:5173"], methods=["GET", "POST"], supports_credentials=True)

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

if __name__ == "__main__":
    app.run(debug=True)
