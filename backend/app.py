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
try:
    # Assumes running from workspace root or backend/ has access relative to root
    kb_path = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'quinn-knowledge.txt') 
    # More robust path: os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'frontend', 'quinn-knowledge.txt'))
    if not os.path.exists(kb_path):
         kb_path = 'frontend/quinn-knowledge.txt' # Fallback if relative path fails

    with open(kb_path, 'r', encoding='utf-8') as f:
        knowledge_base = f.read()
    if knowledge_base:
        print(f"Knowledge base loaded successfully ({len(knowledge_base)} characters).")
    else:
        print("Warning: Knowledge base file loaded but is empty.")
except FileNotFoundError:
    print(f"Warning: Knowledge base file not found at {kb_path}. AI assistant might lack specific procedure knowledge.")
except Exception as e:
    print(f"Error loading knowledge base: {e}")

app = Flask(__name__)
CORS(app)

# --- Simple System Prompt ---
system_prompt = f"""
You are a helpful and friendly AI assistant for a cosmetic procedures clinic. 
Your goal is to answer visitor questions about procedures and help them schedule appointments.

Use the following knowledge base about the clinic's procedures to answer questions accurately. If the information is not in the knowledge base, say that you don't have the specific detail but can provide general information or help schedule a consultation.

Do not make up information not present in the knowledge base.
If the user wants to schedule an appointment, guide them through the process by asking for the desired procedure and preferred time/date. (Note: Actual calendar booking is not implemented yet, just handle the conversation part).

Knowledge Base:
--- START KNOWLEDGE BASE ---
{knowledge_base}
--- END KNOWLEDGE BASE ---

Keep your responses concise and helpful.
"""

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'reply': 'Invalid message'}), 400

    if not llm_configured or not model:
        # Fallback to simple echo if LLM is not configured
        bot_reply = f"LLM not configured. You said: '{user_message}'"
        return jsonify({'reply': bot_reply})

    try:
        # --- LLM Interaction ---
        # For a real app, you would manage conversation history here
        # Example: history.append({"role": "user", "parts": [user_message]})

        # Construct the prompt for the LLM
        # In a stateful app, you'd pass the history to chat.start_chat(history=...)
        full_prompt = system_prompt + "\n\nUser: " + user_message

        response = model.generate_content(full_prompt)
        bot_reply = response.text

        # Example: history.append({"role": "model", "parts": [bot_reply]})

    except Exception as e:
        print(f"Error generating LLM response: {e}")
        bot_reply = "Sorry, I encountered an error trying to process your request."

    return jsonify({'reply': bot_reply})

# --- TODO: Google Calendar Integration ---
# 1. Add authentication flow (OAuth 2.0 or Service Account)
# 2. Implement function to list available slots
# 3. Implement function to create calendar events

if __name__ == '__main__':
    # Note: For development only. Use a production WSGI server (like Gunicorn) for deployment.
    app.run(debug=True, port=5001) # Using port 5001 to avoid potential conflicts 