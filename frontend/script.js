const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');

// Replace with your actual backend URL if different
const backendUrl = 'http://127.0.0.1:5001/chat';

function addMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', sender === 'user' ? 'user-message' : 'bot-message');
    messageElement.textContent = message;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to bottom
}

async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;

    addMessage(message, 'user');
    userInput.value = ''; // Clear input

    try {
        const response = await fetch(backendUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        });

        if (!response.ok) {
            // Handle HTTP errors (e.g., 400, 500)
            console.error('Error from backend:', response.status, await response.text());
            addMessage(`Error: Could not reach the bot (Status: ${response.status})`, 'bot');
            return;
        }

        const data = await response.json();
        if (data.reply) {
            addMessage(data.reply, 'bot');
        } else {
            addMessage('Received an empty reply from the bot.', 'bot');
        }

    } catch (error) {
        // Handle network errors (e.g., server down)
        console.error('Network error:', error);
        addMessage('Error: Could not connect to the chatbot service.', 'bot');
    }
}

// Event Listeners
sendButton.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter') {
        sendMessage();
    }
});

// Initial greeting (optional)
// addMessage("Hello! How can I help you today?", 'bot'); 