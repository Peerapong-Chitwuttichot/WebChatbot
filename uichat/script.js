const socket = new WebSocket('ws://localhost:8080');

const messageInput = document.getElementById('message-input');
const sendButton = document.getElementById('send-button');
const messagesList = document.getElementById('messages');

socket.addEventListener('message', function (event) {
    const message = document.createElement('li');
    message.textContent = event.data;
    messagesList.appendChild(message);
    messagesList.scrollTop = messagesList.scrollHeight;
});

sendButton.addEventListener('click', function () {
    const message = messageInput.value;
    if (message) {
        socket.send(message);
        messageInput.value = '';
    }
});
document.addEventListener('DOMContentLoaded', () => {
    const chatWindow = document.getElementById('chatWindow');
    const userInput = document.getElementById('userInput');
    const sendButton = document.getElementById('sendButton');

    // Function to add a new message to the chat window
    function addMessage(message, isUser = false) {
        const messageElement = document.createElement('p');
        messageElement.textContent = message;
        if (isUser) {
            messageElement.classList.add('user-message');
        }
        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight; // Scroll to the bottom
    }

    // Event listener for the send button
    sendButton.addEventListener('click', () => {
        const message = userInput.value.trim();
        if (message !== '') {
            addMessage(message, true);
            userInput.value = '';
            // Here you can add logic to respond to the user's message
            setTimeout(() => {
                addMessage('Bot response: ' + message);
            }, 500);
        }
    });

    // Optional: Send message when pressing "Enter"
    userInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            sendButton.click();
        }
    });
});
document.addEventListener('DOMContentLoaded', () => {
    const chatWindow = document.getElementById('chatWindow');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');

    // Function to add a message to the chat window
    function addMessage(message, isUser = false) {
        const messageElement = document.createElement('div');
        messageElement.classList.add('chat-message');
        if (isUser) {
            messageElement.classList.add('user');
        }
        messageElement.textContent = message;
        chatWindow.appendChild(messageElement);
        chatWindow.scrollTop = chatWindow.scrollHeight; // Scroll to the bottom
    }

    // Event listener for the send button
    sendButton.addEventListener('click', () => {
        const message = messageInput.value.trim();
        if (message !== '') {
            addMessage(message, true);
            messageInput.value = '';
            
            // Simulate a bot response
            setTimeout(() => {
                addMessage('Bot: ' + message);
            }, 500);
        }
    });

    // Optional: Send message on Enter key press
    messageInput.addEventListener('keydown', (event) => {
        if (event.key === 'Enter') {
            sendButton.click();
        }
    });
});
