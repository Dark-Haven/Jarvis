import time
import streamlit as st
from google import genai
from google.genai import types
from dotenv import load_dotenv

# Load environmental configurations
load_dotenv()
if "client" not in st.session_state:
    st.session_state.client = genai.Client()

# Set up browser window options
st.set_page_config(page_title="Jarvis AI", page_icon="🤖", layout="centered")

def load_css(file_path):
    """Helper function to read external CSS files and inject them into Streamlit"""
    try:
        with open(file_path, "r") as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"System Error: Style asset missing at {file_path}")

# Inject our external style modular sheets
load_css("css/base.css")
load_css("css/chat.css")
load_css("css/loader.css")

st.title("Jarvis Interface")

AI_SYSTEM_RULES = """You are Jarvis, a highly intelligent, sarcastic, and witty AI assistant.
- You must always address the user as 'Sir'.
- Keep your answers extremely concise and clear.
- Use engineering or tech-focused metaphors when appropriate.
- Ur cool so act like it and you should know all marvel fan theories and movies explicably"""

ai_config = types.GenerateContentConfig(
    system_instruction=AI_SYSTEM_RULES,
    temperature=0.7,
)

# Preserve global session context states across updates
if "chat" not in st.session_state:
    st.session_state.chat = st.session_state.client.chats.create(
        model="gemini-2.5-flash", 
        config=ai_config
    )
    st.session_state.messages = []

# Map down prior conversation logs
for msg in st.session_state.messages:
    # Match the avatar variable depending on who sent the message
    current_avatar = USER_AVATAR if msg["role"] == "user" else BOT_AVATAR
    
    with st.chat_message(msg["role"], avatar=current_avatar):
        st.markdown(msg["content"])

# Capture upcoming commands
if prompt := st.chat_input("Enter Prompt :"):
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Render target automation sequence
    with st.chat_message("assistant"):
        loader_placeholder = st.empty()
        loader_placeholder.markdown('<p class="thinking-text">Jarvis is compiling data packages...</p>', unsafe_allow_html=True)
        
        try:
            response = st.session_state.chat.send_message(prompt)
            output_text = response.text
        except Exception as e:
            output_text = f"API ERROR: {str(e)}"
        
        loader_placeholder.empty()
        
        # Real-time console terminal simulation output loop
        response_placeholder = st.empty()
        full_response = ""
        for char in output_text:
            full_response += char
            response_placeholder.markdown(full_response + "▌")
            time.sleep(0.008)
        response_placeholder.markdown(full_response)
        
    st.session_state.messages.append({"role": "assistant", "content": output_text})