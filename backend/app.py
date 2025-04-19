import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables (e.g., for API keys)
load_dotenv()

# --- Configuration ---
# Try to configure Generative AI
try:
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel('gemini-1.5-flash') # Using flash for speed/cost
    print("Google Generative AI configured successfully.")
    llm_configured = True
except Exception as e:
    print(f"Error configuring Google Generative AI: {e}")
    print("LLM features will be disabled. Ensure GOOGLE_API_KEY is set correctly.")
    model = None
    llm_configured = False

# Load Knowledge Base
knowledge_base = ""
kb_path = "" # Initialize kb_path
try:
    # Path relative to workspace root (where app.py is usually run from)
    kb_path = 'quinn-knowledge.md' 
    
    # Optional: More robust path if script might run from backend/ dir itself
    # alt_kb_path = os.path.join(os.path.dirname(__file__), '..', 'quinn-knowledge.md')
    # if not os.path.exists(kb_path) and os.path.exists(alt_kb_path):
    #      kb_path = alt_kb_path

    with open(kb_path, 'r', encoding='utf-8') as f:
        knowledge_base = f.read()
    if knowledge_base:
        print(f"Knowledge base loaded successfully from '{os.path.abspath(kb_path)}' ({len(knowledge_base)} characters).")
    else:
        print(f"Warning: Knowledge base file loaded from '{os.path.abspath(kb_path)}' but is empty.")
except FileNotFoundError:
    print(f"Warning: Knowledge base file not found. Looked for '{kb_path}' relative to the execution directory. AI assistant might lack specific procedure knowledge.")
except Exception as e:
    print(f"Error loading knowledge base: {e}")

app = Flask(__name__)
CORS(app)

# --- System Prompt for the Chatbot ---
system_prompt = f"""
You are a helpful and friendly AI assistant for a cosmetic procedures clinic named Quinn. 
Your goal is to answer visitor questions about procedures and help them schedule appointments only when they explicitly ask to make an appointment.

Use the following knowledge base about the clinic's procedures to answer questions accurately. If the information is not in the knowledge base, try to still answer the question, but don't make up information, if you need clarification.

Do not make up information. If you need
If the user wants to schedule an appointment, guide them through the process by asking for the desired procedure and preferred time/date. (Note: Actual calendar booking is not implemented yet, just handle the conversation part).

Only give responses that are applicable to Medical Aesthetics.

Refer to previous messages in the conversation when relevant to provide contextually appropriate responses.


Knowledge Base:
--- START KNOWLEDGE BASE ---
{knowledge_base}
--- END KNOWLEDGE BASE ---

Keep your responses concise and helpful.
"""

# --- Global Chat Session ---
# WARNING: This creates a SINGLE global chat session.
# All users interacting with the app will share the same conversation history.
# For a real application, you would need session management (e.g., store chat sessions per user ID).
chat_session = None
if llm_configured and model:
    try:
        # Initialize the chat session with the system prompt
        chat_session = model.start_chat(history=[
             {"role": "user", "parts": [system_prompt]},
             {"role": "model", "parts": ["Okay, I understand. I'm ready to help answer questions about our cosmetic procedures or schedule an appointment."]}
        ])
        print("Chat session initialized.")
    except Exception as e:
        print(f"Error initializing chat session: {e}")
        llm_configured = False # Disable LLM features if chat fails to init


@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'reply': 'Invalid message'}), 400

    if not llm_configured or not model or not chat_session:
        # Fallback if LLM is not configured or chat session failed
        # In a real app, you might attempt to re-initialize or provide a more specific error.
        bot_reply = f"LLM not configured or session failed. You said: '{user_message}'"
        return jsonify({'reply': bot_reply})

    try:
        # --- LLM Interaction using Chat Session ---
        # Send the user message to the ongoing chat session
        response = chat_session.send_message(user_message)
        bot_reply = response.text

    except Exception as e:
        print(f"Error generating LLM response: {e}")
        # Consider more specific error handling (e.g., rate limits, content filtering)
        bot_reply = "Sorry, I encountered an error trying to process your request."
        # You might want to reset or clear the chat_session history here in some error cases

    return jsonify({'reply': bot_reply})

# --- TODO: Google Calendar Integration ---
# 1. Add authentication flow (OAuth 2.0 or Service Account)
# 2. Implement function to list available slots
# 3. Implement function to create calendar events

# --- TODO: Session Management ---
# Replace the global `chat_session` with a mechanism to handle multiple concurrent users.
# Options: Flask session, in-memory dictionary keyed by session ID, database storage.

if __name__ == '__main__':
    # Note: For development only. Use a production WSGI server (like Gunicorn) for deployment.
    app.run(debug=True, port=5001) # Using port 5001 to avoid potential conflicts 