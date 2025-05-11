import streamlit as st
import requests
import json

# --- Configuration ---
API_URL = "http://localhost:8000/chat"  # Replace with your API endpoint

# --- Initialize Session State ---
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = "default_session"  # You might want to generate a unique ID

# --- Function to Call the API ---
def call_chat_api(question, session_id, model="gemini-2.0-flash"):
    payload = {
        "question": question,
        "session_id": session_id,
        "model": model
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for bad status codes
        data = response.json()
        return data.get("answer")
    except requests.exceptions.RequestException as e:
        return f"Error calling API: {e}"
    except json.JSONDecodeError:
        return "Error decoding API response."
    except Exception as e:
        return f"An unexpected error occurred: {e}"

# --- Streamlit UI ---
st.markdown("<h1 style='color: #17a2b8;'><span style='font-size: 1.8em;'>👩‍⚕️</span> Madie</h1><h4>Find the Right Doctor for You</h4>", unsafe_allow_html=True)

# Display chat history
for role, message in st.session_state.chat_history:
    with st.chat_message(role):
        st.markdown(message)  # Use st.markdown for better formatting

# User input
prompt = st.chat_input("Say something")

if prompt:
    st.session_state.chat_history.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)  # Use st.markdown for consistency

    # Call the API and display the response
    with st.chat_message("ai"):
        with st.spinner("Thinking..."):
            ai_response = call_chat_api(prompt, st.session_state.session_id)
        st.markdown(ai_response)  # Use st.markdown to render line breaks, etc.
        st.session_state.chat_history.append(("ai", ai_response))