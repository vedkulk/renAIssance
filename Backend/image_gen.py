import os
import random
from dotenv import load_dotenv
import requests
import json

# Load environment variables
load_dotenv()

WORQHAT_API_KEY = os.getenv("WORQHAT_API_KEY")


def translate_text(input_text, target_language, model_name="aicon-v4-nano-160824"):
    """
    Translate input text to the target language using WorqHat's API.

    Args:
        input_text (str): Text to be translated.
        target_language (str): Target language (e.g., english, hindi, french).
        model_name (str): Model to use for translation.

    Returns:
        str: Translated text or an error message.
    """
    try:
        response = requests.post(
            "https://api.worqhat.com/api/ai/content/v4", #url for api_end_point
            headers={"Authorization": f"Bearer {WORQHAT_API_KEY}"}, #authorisation of api
            json={
                "question": f"Translate this text to {target_language}: {input_text}", 
                "model": model_name,
            },
        )
        response_data = response.json()
        if response.status_code == 200:
            # Extract and return only the content
            return response_data.get("content", "Translation not available.")
        else:
            return f"Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"An exception occurred: {e}"

words = {
    "Everyday Objects": [
        "Chair", "Table", "Cup", "Plate", "Spoon", "Knife", "Fork", "Bottle", "Bag", 
        "Pen", "Pencil", "Notebook", "Phone", "Key", "Wallet", "Glasses", "Watch", 
        "Shoes", "Socks", "Hat"
    ],
    "Food and Drinks": [
        "Apple", "Banana", "Orange", "Bread", "Rice", "Egg", "Milk", "Coffee", 
        "Tea", "Water", "Cheese", "Cake", "Pizza", "Burger", "Sandwich", "Salad"
    ],
    "Household Items": [
        "Bed", "Pillow", "Blanket", "Mirror", "Clock", "Lamp", "Door", "Window", 
        "Fan", "Television", "Refrigerator", "Microwave", "Soap", "Shampoo", 
        "Towel", "Toothbrush"
    ],
    "Animals": [
        "Cat", "Dog", "Bird", "Fish", "Cow", "Horse", "Elephant", "Rabbit", 
        "Butterfly", "Snake"
    ],
    "Transportation": [
        "Car", "Bike", "Bus", "Train", "Airplane", "Boat", "Truck", "Bicycle", 
        "Scooter", "Taxi"
    ],
    "Places": [
        "Home", "School", "Market", "Park", "Hospital", "Library", "Office", 
        "Bank", "Airport", "Restaurant"
    ],
    "Nature": [
        "Tree", "Flower", "Grass", "Mountain", "River", "Cloud", "Sun", "Moon", 
        "Star", "Rain"
    ],
    "Clothing": [
        "Shirt", "Trousers", "Skirt", "Dress", "Jacket", "Gloves", "Scarf", 
        "Belt", "Uniform", "Suit"
    ],
    "Colors": [
        "Red", "Blue", "Green", "Yellow", "Orange", "Pink", "White", "Black", 
        "Purple", "Brown"
    ],
    "Actions (Verbs)": [
        "Walk", "Run", "Eat", "Drink", "Sleep", "Read", "Write", "Play", 
        "Swim", "Dance"
    ],
    "Emotions": [
        "Happy", "Sad", "Angry", "Surprised", "Scared", "Excited", "Confused", 
        "Tired", "Bored", "Calm"
    ],
    "Technology": [
        "Computer", "Laptop", "Tablet", "Smartphone", "Camera", "Printer", 
        "Headphones", "Charger", "Mouse", "Keyboard"
    ]
}

def translate_text(input_text, target_language, model_name="aicon-v4-nano-160824"):
    """
    Translate input text to the target language using WorqHat's API.

    Args:
        input_text (str): Text to be translated.
        target_language (str): Target language (e.g., english, hindi, french).
        model_name (str): Model to use for translation.

    Returns:
        str: Translated text or an error message.
    """
    try:
        response = requests.post(
            "https://api.worqhat.com/api/ai/content/v4",  # URL for the API endpoint
            headers={"Authorization": f"Bearer {WORQHAT_API_KEY}"},  # Authorization
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

def generate_image_from_text(input_text):
    """
    Generate a realistic square image from the input text using WorqHat's Image Generation API v3.

    Args:
        input_text (str): Text prompt for generating an image.

    Returns:
        str: Image URL or an error message.
    """
    if not WORQHAT_API_KEY:
        return "Error: API key not found. Please check your .env file."

    try:
        url = "https://api.worqhat.com/api/ai/images/generate/v3"
        payload = {
            "prompt": [input_text],
            "image_style": "Realistic",
            "orientation": "Square",
            "output_type": "url"
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {WORQHAT_API_KEY}'
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200:
            response_data = response.json()
            if 'images' in response_data and len(response_data['images']) > 0:
                return response_data['images'][0]  # Return the first image URL
            else:
                return f"Image URL found in response: {response_data}"
           
        else:
            error_data = response.json()
            return f"API Error: {error_data.get('message', response.text)}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

def select_scenario():
    print("Select a scenario:")
    scenarios = list(words.keys())
    for i, scenario in enumerate(scenarios, 1):
        print(f"{i}. {scenario}")
    choice = int(input("Enter the number of your chosen scenario: "))
    if choice < 1 or choice > len(scenarios):
        print("Invalid choice. Please select a valid option.")
        return select_scenario()
    return scenarios[choice - 1]

def display_images(scenario):
    target_language = input("Enter the target language for translation (e.g., english, hindi, french): ").strip().lower()
    items = words[scenario]
    random.shuffle(items)
    for item in items:
        translated_text = translate_text(item, target_language)
        print(f"Generating image for: {item} ({translated_text})")
        result = generate_image_from_text(item)
        print("\nImage URL:", result)
        next_image = input("Do you want to see the next image? (y/n): ").strip().lower()
        if next_image != 'y':
            break

if __name__ == "__main__":
    scenario = select_scenario()
    display_images(scenario)
