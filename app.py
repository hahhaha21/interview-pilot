import streamlit as st
import speech_recognition as sr
import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini API
if api_key:
    genai.configure(api_key=api_key)
    # Reverting to the exact model name that worked in your initial Korean version
    try:
        model = genai.GenerativeModel("gemini-2.5-flash-preview-09-2025")
    except Exception as e:
        st.error(f"Failed to initialize Gemini model: {str(e)}")
else:
    st.error("API Key not found. Please check your .env file.")

def get_ai_response(question, level, role):
    """Generate tailored interview answers using Gemini"""
    prompt = f"""
    You are a professional Interview Coach. 
    Context: The user is in an interview and received a question from the interviewer.
    Question: "{question}"
    User Info: Applied Position - {role}, Experience Level - {level}
    
    Requirements:
    1. Briefly analyze the intent of this question.
    2. Provide key bullet points for the best answer based on the {level} level.
    3. Provide a natural, spoken-style example answer.
    4. Respond entirely in English in a professional yet encouraging tone.
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"An error occurred during content generation: {str(e)}"

# Streamlit UI Configuration
st.set_page_config(page_title="AI Interview Pilot", page_icon="🎤")
st.title("🎤 AI Real-time Interview Assistant")
st.caption("Listen to the interviewer's question and get real-time answer guidance.")

# Sidebar Configuration
with st.sidebar:
    st.header("Settings")
    role = st.text_input("Target Job Position", value="Software Developer")
    level = st.selectbox("Experience Level", ["Intern", "Junior (Entry-level)", "Senior", "Career Changer"])
    st.divider()
    st.info("This app recognizes speech in real-time. Please ensure your microphone is working.")

# Session State for Speech Recognition
if "question_text" not in st.session_state:
    st.session_state.question_text = ""

# Speech Recognition Function
def recognize_speech():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("🎤 Listening... Please speak now.")
        try:
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
            # Recognizing speech in English
            text = r.recognize_google(audio, language="en-US")
            st.session_state.question_text = text
        except sr.WaitTimeoutError:
            st.warning("Listening timed out. Please try again.")
        except Exception as e:
            st.error(f"Speech recognition error: {str(e)}")
            st.info("If the microphone is unavailable, please type your question manually.")

# Main Layout
col1, col2 = st.columns([1, 1])

with col1:
    if st.button("🎤 Start Listening to Interviewer", use_container_width=True):
        recognize_speech()
    
    question = st.text_area("Recognized Question (Editable):", value=st.session_state.question_text, height=150)

with col2:
    if st.button("💡 Generate Answer Guide", type="primary", use_container_width=True):
        if question:
            with st.spinner("Thinking of the best response..."):
                answer = get_ai_response(question, level, role)
                st.markdown("### 💡 AI Recommended Guide")
                st.write(answer)
        else:
            st.warning("Please record a question or type one first.")

st.divider()
st.caption("© 2026 Interview Pilot Project - Developed for Class Assignment (Prof. Wojciech Czart)")