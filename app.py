import os
import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv('gemini.env')                               
Gemini_Api_Key = os.getenv("Gemini_Api_Key")  

if not Gemini_Api_Key:
    st.error("Missing Gemini_Api_Key in your .env file")
    st.stop()

genai.configure(api_key=Gemini_Api_Key)

MODEL_NAME = "models/gemini-2.0-flash-lite"  
model = genai.GenerativeModel(MODEL_NAME)

st.set_page_config(page_title="Gemini Lite Chat", page_icon="💬")
st.title("Chat with Gemini Lite")

#Create/restore chat session 
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

chat = st.session_state.chat   

def to_streamlit_role(gemini_role: str) -> str:
    """Gemini uses 'user'/'model'; Streamlit expects 'user'/'assistant'."""
    return "assistant" if gemini_role == "model" else gemini_role

#Render existing history 
for msg in chat.history:
    with st.chat_message(to_streamlit_role(msg.role)):
        st.markdown(msg.parts[0].text)

# Handle new user input 
prompt = st.chat_input("Ask Gemini Lite …")

if prompt:
    # showuser message
    with st.chat_message("user"):
        st.markdown(prompt)

    # send Gemini and response
    response = chat.send_message(prompt)

    # display reply
    with st.chat_message("assistant"):
        st.markdown(response.text)
