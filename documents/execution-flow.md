# Chatbot MVP Execution Flow

This document outlines the step-by-step execution flow of the chatbot MVP, detailing the interactions between the frontend, backend, and the LLM.

## Startup (Backend)

1.  `Backend (app.py)`: Application starts.
2.  `Backend (app.py)`: Loads environment variables (including `GOOGLE_API_KEY`) from `.env` file using `load_dotenv()`.
3.  `Backend (app.py)`: Attempts to configure the Google Generative AI client (`genai`) using the API key.
4.  `Backend (app.py)`: Attempts to load the `quinn-knowledge.txt` file into the `knowledge_base` variable.
5.  `Backend (app.py)`: Constructs the `system_prompt`, incorporating the loaded `knowledge_base`.
6.  `Backend (app.py)`: Starts the Flask development server.

## User Interaction & Backend Communication

1.  **Initialization (Frontend)**
    *   `User`: Opens `frontend/index.html` in a web browser.
    *   `Browser`: Loads associated `frontend/style.css` and `frontend/script.js`.

2.  **Sending a Message**
    *   `User`: Types a message into the input field (`#user-input` in `index.html`).
    *   `User`: Clicks the "Send" button (`#send-button`) or presses Enter.
    *   `Frontend (script.js)`: Event listener triggers the `sendMessage()` function.
    *   `Frontend (script.js)`: `sendMessage()` retrieves the message from `#user-input`.
    *   `Frontend (script.js)`: `sendMessage()` calls `addMessage()` to display the user's message in the chat box (`#chat-box`).
    *   `Frontend (script.js)`: `sendMessage()` clears the `#user-input` field.
    *   `Frontend (script.js)`: `sendMessage()` initiates an asynchronous `fetch` POST request to the backend endpoint (`http://127.0.0.1:5001/chat`) with the message in the JSON body (e.g., `{"message": "Tell me about Botox"}`).

3.  **Backend Processing (LLM Integration)**
    *   `Backend (app.py)`: Flask server receives the POST request at the `/chat` route.
    *   `Backend (app.py)`: The `chat()` route handler function is invoked.
    *   `Backend (app.py)`: Extracts the `message` from the incoming request's JSON payload.
    *   `Backend (app.py)`: Performs basic validation (checks if the message is not empty).
    *   `Backend (app.py)`: Checks if the LLM (`model`) was configured successfully during startup. If not, returns a fallback message.
    *   `Backend (app.py)`: Constructs the `full_prompt` by combining the pre-defined `system_prompt` (which includes the knowledge base) and the current `user_message`.
    *   `Backend (app.py)`: Calls the Google Generative AI API (`model.generate_content()`) with the `full_prompt`.
    *   `Google AI API`: Processes the request using the specified model (e.g., `gemini-1.5-flash`) and generates a response based on the prompt and its training data.
    *   `Backend (app.py)`: Receives the response object from the Google AI API.
    *   `Backend (app.py)`: Extracts the text content (`response.text`) from the response.
    *   `Backend (app.py)`: Handles potential errors during API call and sets an appropriate error message if needed.
    *   `Backend (app.py)`: Constructs a JSON response containing the generated `reply` (e.g., `{"reply": "Botox is a medication injected..."}`).
    *   `Backend (app.py)`: Flask sends the JSON response back to the frontend.

4.  **Displaying the Response**
    *   `Frontend (script.js)`: The `fetch` call in `sendMessage()` receives the response from the backend.
    *   `Frontend (script.js)`: Checks if the response status is OK (e.g., 200).
    *   `Frontend (script.js)`: Parses the JSON data from the response body.
    *   `Frontend (script.js)`: Extracts the `reply` string from the parsed data.
    *   `Frontend (script.js)`: Calls `addMessage()` to display the bot's reply in the chat box (`#chat-box`).

*(Note: This flow includes LLM integration for conversation. Google Calendar API interactions for actual scheduling are not yet implemented.)*
