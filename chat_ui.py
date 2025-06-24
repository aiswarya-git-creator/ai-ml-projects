import streamlit as st
import requests

st.title("🧠 Mental Health Chatbot")

user_input = st.text_input("How are you feeling today?")

if st.button("Send") and user_input:
    with st.spinner("Thinking..."):
        try:
            response = requests.post("http://localhost:5000/chat", json={"message": user_input})
            #st.write("Status code:", response.status_code)
            #st.write("Raw response text:", response.text)

            # Try parsing JSON safely
            data = response.json()
            bot_reply = data.get("response", "Sorry, no response received.")
        except Exception as e:
            st.error(f"Error processing response: {e}")
            bot_reply = "Sorry, something went wrong while processing the response."

        st.text_area("Bot says:", value=bot_reply, height=500)
