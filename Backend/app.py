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

WORQHAT_API_KEY=os.getenv("WORQHAT_API_KEY")

def speech_to_text(audio_path):
    with open(audio_path, "rb") as audio_file:
        response=requests.post(
            "https://api.worqhat.com/api/ai/content/v4", #Multimodal Input Conversational
            headers={"Authorization": f"Bearer {WORQHAT_API_KEY}"},
            files={"file": audio_file},
            data={
                "question":"Transribe this audio",
                "model":"aion-v4-nano-160824"
            },
        )
    return response.json().get("text","Speech-To-text conversion failed")

def main():
    audio_path='xyz'
    transcription = speech_to_text(audio_path)
    print("Transcription : ", transcription)

if __name__=='__main__':
    main()
