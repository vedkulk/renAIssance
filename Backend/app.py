from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import pandas as pd
from reportlab.pdfgen import canvas #certificate generation 
from langdetect import detect
import requests


load_dotenv() #load the env variables (Api key)

# Initialise flask
app = Flask(__name__)
CORS(app)

WORQHAT_API_KEY = os.getenv("WORQHAT_API_KEY")

def speech_to_text(audio_path):
    with open(audio_path, "rb") as audio_file:
        response = requests.post(
    "https://api.worqhat.com/api/ai/content/v4",
    headers={"Authorization": f"Bearer {WORQHAT_API_KEY}"},
    files={"file": audio_file},
    data={
        "question": "Transribe this audio",
        "model": "aicon-v4-large-160824"
        },
    )
        
def main():
    audio_path = r'C:\Users\sheet\OneDrive\Desktop\Jinesh\RenAi\renAIssance\Backend\example.mp4'
    transcription = speech_to_text(audio_path)
    print("Transcription : ", transcription)

if __name__=='__main__':
    main()
