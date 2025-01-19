import os
import google.generativeai as genai
import re
from datetime import datetime
from google.cloud import translate_v2 as translate

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
    return translate.Client.from_service_account_json("gen-lang-client-0182388257-027b6c8204af.json")

def clean_response(response_text):
    """Clean the response to remove unnecessary text"""
    cleaned = re.sub(r'\[.*?\]', '', response_text)  # Remove square bracket content
    cleaned = cleaned.split("Suggested responses")[0] if "Suggested responses" in cleaned else cleaned
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

def translate_text(client, text, target_language):
    """Translate the given text to the target language"""
    result = client.translate(text, target_language=target_language)
    return result["translatedText"]

def handle_clarification(user_input):
    """Provide clarifications for unclear input."""
    clarifications = [
        "I didn’t quite catch that. Are you asking about a specific route or schedule?",
        "Could you rephrase or provide more details?",
        "I’m here to help! Are you looking for ticket prices or directions?"
    ]
    return clarifications[hash(user_input) % len(clarifications)]

def run_transportation_conversation():
    try:
        model = setup_gemini()
        translation_client = setup_translation_client()

        # Define the context for the conversation
        context = """You are a helpful and friendly public transportation guide. 
        Assist the customer in understanding directions, routes, ticket types, and schedules. 
        Provide clear and simple responses to their questions about public transport. 
        Here is some example data you can use in your responses:

        - Routes:
            1. Bus 101: Downtown to Central Park (Every 15 minutes)
            2. Train A: Airport to City Center (Every 30 minutes)
            3. Bus 202: University to Shopping Mall (Every 20 minutes)

        - Ticket Prices:
            - Single Ride: $2.50
            - Day Pass: $7.00
            - Weekly Pass: $25.00

        Include helpful suggestions about nearby landmarks when giving directions."""

        # Start chat and initialize with context
        chat = model.start_chat(history=[])
        chat.send_message(context)

        preferred_language = input("Please enter your preferred language (e.g., fr for French, es for Spanish): ").strip()

        print(f"\nGuide: {get_greeting()} How can I assist you with public transportation today?")

        while True:
            user_input = input("\nYou: ").strip()

            if not user_input:
                print("\nGuide: I didn't quite catch that. Could you please repeat?")
                continue

            if user_input.lower() in ['goodbye', 'exit', 'quit']:
                print("\nGuide: Thank you for using public transportation! Have a safe journey!")
                break

            try:
                # Translate user input to English if necessary
                user_input_translated = translate_text(translation_client, user_input, 'en')

                # Translate user message back to their preferred language for confirmation
                user_input_confirmed = translate_text(translation_client, user_input_translated, preferred_language)
                print(f"\nTranslated user Text: {user_input_confirmed}")

                # Get response from Gemini model
                response = chat.send_message(f"Customer: {user_input_translated}\nRespond naturally without showing instructions or context.")
                if response and hasattr(response, 'text'):
                    cleaned_response = clean_response(response.text)

                    if not cleaned_response or "I didn't quite understand" in cleaned_response:
                        clarification = handle_clarification(user_input)
                        translated_clarification = translate_text(translation_client, clarification, preferred_language)
                        print(f"\nGuide: {translated_clarification} \n (English: {clarification})")
                    else:
                        translated_response = translate_text(translation_client, cleaned_response, preferred_language)
                        print(f"\nGuide: {translated_response}  \n (English: {cleaned_response})")
                else:
                    clarification = handle_clarification(user_input)
                    translated_clarification = translate_text(translation_client, clarification, preferred_language)
                    print(f"\nGuide: {translated_clarification} \n (English: {clarification})")

            except Exception as e:
                print("\nGuide: I apologize for the technical difficulty. How else can I help you today?")

    except Exception as e:
        print(f"System Error: {str(e)}")
        print("Please ensure you have installed the google-generativeai and google-cloud-translate packages, and have valid API keys.")

if __name__ == "__main__":
    run_transportation_conversation()
