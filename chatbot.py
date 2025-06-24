import os
import requests
from dotenv import load_dotenv

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def get_groq_response(user_input):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [
        {"role": "system", "content": "You are a kind, supportive mental health assistant. Be empathetic and never judgmental."},
        {"role": "user", "content": user_input}
    ]

    data = {
        "model": "gemma2-9b-it",

        "messages": messages,
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        print("Groq API response status:", response.status_code)

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            print("Groq error:", response.text)  # Print actual error
            return "Sorry, something went wrong with the AI response."

    except Exception as e:
        print("Exception occurred:", str(e))
        return "Sorry, something went wrong with the AI response."
