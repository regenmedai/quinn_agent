# Google Calendar Chatbot MVP

This project is a Minimum Viable Product (MVP) for a chatbot that integrates with the Google Calendar API to schedule appointments and provide information.

## Structure

- `/backend`: Contains the Python Flask server.
    - `app.py`: The main Flask application.
    - `requirements.txt`: Python dependencies.
- `/frontend`: Contains the simple web-based chat interface.
    - `index.html`: The HTML structure.
    - `style.css`: CSS for styling.
    - `script.js`: JavaScript for frontend logic (sending/receiving messages).
- `.env.example`: Example environment variables (copy to `.env` and fill in).
- `README.md`: This file.

## Setup & Running

### Prerequisites

- Python 3.x
- `pip` (Python package installer)
- Google Cloud Project with Calendar API enabled.
- OAuth 2.0 Credentials (Client ID and Secret) or a Service Account key (`.json` file) for Google Calendar API access (via `GOOGLE_APPLICATION_CREDENTIALS`).
- Google AI API Key for the LLM (Gemini) access (via `GOOGLE_API_KEY`). You can obtain one from [Google AI Studio](https://aistudio.google.com/app/apikey).

### Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```
2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Set up environment variables:**
    - Copy `.env.example` from the root directory to `backend/.env`.
    - Edit `backend/.env` and add your Google Cloud credentials information (e.g., `GOOGLE_APPLICATION_CREDENTIALS=path/to/your/credentials.json`) and your Google AI API Key (e.g., `GOOGLE_API_KEY=YOUR_API_KEY_HERE`). **Note:** Calendar credentials are not used yet.

5.  **Run the Flask server:**
    ```bash
    flask run --port 5001
    # Or: python app.py
    ```
    The backend server should now be running on `http://127.0.0.1:5001`.

### Frontend Setup

1.  **Open the `frontend/index.html` file in your web browser.** You can usually do this by double-clicking the file or using a simple web server (like Python's built-in one for testing):
    ```bash
    cd frontend
    python -m http.server 8000 
    # Then navigate to http://localhost:8000 in your browser
    ```

### Using the Chatbot

- Open the `index.html` page.
- Type a message in the input box and click "Send" or press Enter.
- The frontend will send the message to the backend, and the backend's (currently placeholder) response will appear in the chat.

## Next Steps (TODO)

- **Backend:**
    - Implement Google Calendar API authentication (OAuth 2.0 for user delegation or Service Account for backend access).
    - Add functions to interact with the Calendar API (check availability, create events).
    - Improve intent recognition beyond simple keyword matching.
    - Add state management to handle multi-turn conversations (e.g., asking for procedure, then time, then confirming).
    - Implement CORS handling if frontend and backend are served from different origins in production.
- **Frontend:**
    - Improve UI/UX (loading indicators, better error handling). 