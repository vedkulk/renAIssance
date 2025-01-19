import os
import google.generativeai as genai
import re
from datetime import datetime
from google.cloud import translate_v2 as translate

def setup_gemini():
    """Configure Gemini API with the provided key"""
    genai.configure(api_key="AIzaSyC7-YhQoMLVhx2J_S_U_bnp917sqoEZ-JI")

    generation_config = {
        "temperature": 0.5,  # Lower temperature for concise and focused responses
        "top_p": 0.8,       # Encourage higher confidence tokens
        "top_k": 20,        # Smaller range of token selection
        "max_output_tokens": 200,  # Adjust response length for meaningful sentences
    }

    return genai.GenerativeModel(
        model_name="gemini-1.0-pro",
        generation_config=generation_config,
    )

def setup_translation_client():
    """Set up Google Translate API client"""
    return translate.Client.from_service_account_json("gen-lang-client-0182388257-027b6c8204af.json")

def clean_response(response_text):
    """Clean the response to ensure brevity and relevance"""
    cleaned = re.sub(r'\[.*?\]', '', response_text)  # Remove square bracket content
    cleaned = cleaned.split("Suggested responses")[0] if "Suggested responses" in cleaned else cleaned
    cleaned = re.sub(r'Doctor:?|Career Coach:?|Shopkeeper:?|\*+', '', cleaned)  # Remove roles and asterisks
    cleaned = " ".join(cleaned.split()).strip()  # Clean up whitespace
    return cleaned  # Allow full meaningful response

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
        "Could you clarify your request?",
        "Can you rephrase that?",
        "Let me know more details!"
    ]
    return clarifications[hash(user_input) % len(clarifications)]

def run_transport_guide():
    try:
        model = setup_gemini()
        translation_client = setup_translation_client()

        # Define the context for the conversation
        context = """ You are a supportive and knowledgeable career coach. 
Assist the customer in preparing for job interviews by practicing common interview questions, discussing their skills, and explaining workplace etiquette. 
Provide clear, actionable, and motivational responses that boost their confidence. Use the example below to guide your tone and style:

- Example Interaction:
    Customer: "Can you help me answer 'What are your strengths and weaknesses?'"
    Response: "Of course! A good approach is to highlight strengths that align with the job role, like 'I am highly organized and excel at managing projects on tight deadlines.' For weaknesses, mention something you're working to improve, like 'I sometimes focus too much on details, but I’ve been practicing delegating tasks to stay efficient.'"

- Common Interview Questions:
    1. Tell me about yourself.
    2. What are your strengths and weaknesses?
    3. Where do you see yourself in 5 years?
    4. Why do you want to work for our company?
    5. Can you describe a challenging situation you faced and how you resolved it?

- Workplace Etiquette Tips:
    - Arrive 10 minutes early to the interview.
    - Dress professionally (formal or business casual as required).
    - Maintain good posture, eye contact, and a friendly demeanor.
    - Always thank the interviewer at the end of the session.

- Skills and Phrases:
    - Highlight transferable skills such as teamwork, problem-solving, and adaptability.
    - Use phrases like 'I am eager to learn,' 'I take initiative,' and 'I value collaboration.'

Base your responses on the example style, ensuring they are concise, actionable, and tailored to the customer’s specific question or concern."""

        # Start chat and initialize with context
        chat = model.start_chat(history=[])
        chat.send_message(context)

        preferred_language = input("Please enter your preferred language (e.g., fr for French, es for Spanish): ").strip()

        print(f"\nCareer Coach: {get_greeting()} Welcome! How can I assist you today?")

        while True:
            user_input = input("\nYou: ").strip()

            if not user_input:
                print("\nCareer Coach: Could you repeat that?")
                continue

            if user_input.lower() in ['goodbye', 'exit', 'quit']:
                print("\nCareer Coach: Thanks for visiting! Have a great day!")
                break

            try:
                # Translate user input to English if necessary
                user_input_translated = translate_text(translation_client, user_input, 'en')

                # Get response from Gemini model
                response = chat.send_message(f"Customer: {user_input_translated}")

                if response and hasattr(response, 'text'):
                    cleaned_response = clean_response(response.text)

                    if not cleaned_response:
                        clarification = handle_clarification(user_input)
                        translated_clarification = translate_text(translation_client, clarification, preferred_language)
                        print(f"\nCareer Coach: {translated_clarification}")
                        print(f"(English: {clarification})")
                    else:
                        translated_response = translate_text(translation_client, cleaned_response, preferred_language)
                        user_input_translated_back = translate_text(translation_client, user_input, preferred_language)
                        print(f"\nYou (Translated): {user_input_translated_back}")
                        print(f"\nCareer Coach: {translated_response}")
                        print(f"(English: {cleaned_response})")
                else:
                    clarification = handle_clarification(user_input)
                    translated_clarification = translate_text(translation_client, clarification, preferred_language)
                    print(f"\nCareer Coach: {translated_clarification}")
                    print(f"(English: {clarification})")

            except Exception as e:
                print("\nCareer Coach: Sorry, something went wrong. How else can I help?")

    except Exception as e:
        print(f"System Error: {str(e)}")
        print("Please ensure the required packages and API keys are set up correctly.")

if __name__ == "__main__":
    run_transport_guide()
