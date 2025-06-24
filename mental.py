import os
import requests

from flask import Flask, request, jsonify
from chatbot import get_groq_response
import time
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

app = Flask(__name__)

def log_session(user_msg, bot_reply):
    with open("sessions.log", "a") as f:
        f.write(f"[{time.ctime()}]\nUser: {user_msg}\nBot: {bot_reply}\n\n")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"

    }
    data = {
        "model": "gemma2-9b-it",  # ✅ Use only Groq-supported models
        "messages": [
            {"role": "system", "content": (
                "You are a supportive and empathetic mental health assistant. "
                "You must ONLY answer questions related to mental health or emotional support. "
                "If the user's question is not about mental or emotional support, reply with: "
                "'Sorry, I can only help with mental or emotional support questions.'"
            )},
            {"role": "user", "content": user_message}
        ],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=data)
    print("Status:", response.status_code)
    print("Raw text:", response.text)

    try:
        data = response.json()
        bot_reply = data["choices"][0]["message"]["content"]
    except Exception as e:
        print("JSON decode error:", e)
        bot_reply = "Sorry, something went wrong while processing the response."

    return jsonify({"response": bot_reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
