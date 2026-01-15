🎤 AI Interview Pilot

by Haeun Park

A real-time interview assistance application that combines Speech-to-Text (STT) technology with the Gemini API to provide tailored answer guidance during interviews.

🚀 Key Features

Real-time Speech Recognition: Uses the SpeechRecognition library to transcribe interviewer questions instantly.

Tailored Answer Generation: Gemini API suggests optimized answer strategies based on the user's target role and experience level.

Security Management: Safely manages sensitive information (API Keys) using .env files.

🛠 Tech Stack

Language: Python 3.9+
AI/LLM: Google Gemini API (gemini-1.5-flash)
Framework: Streamlit
Audio: SpeechRecognition, PyAudio

⚙️ How to Install & Run

Clone the Repository:

git clone [https://github.com/hahhaha21/interview-pilot.git]
cd interview-pilot


Install Dependencies:
pip install -r requirements.txt

Set Environment Variables:
Create a .env file and enter your GEMINI_API_KEY.

Run the App:
streamlit run app.py

