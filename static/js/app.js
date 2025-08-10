class ChatApp {
    constructor() {
        this.socket = null;
        this.currentUser = null;
        this.users = [];
        this.messages = [];
        
        this.initializeElements();
        this.bindEvents();
        this.connectSocket();
    }

    initializeElements() {
        // Screens
        this.loginScreen = document.getElementById('loginScreen');
        this.chatScreen = document.getElementById('chatScreen');
        
        // Login elements
        this.loginForm = document.getElementById('loginForm');
        this.usernameInput = document.getElementById('usernameInput');
        
        // Chat elements
        this.currentUserSpan = document.getElementById('currentUser');
        this.logoutBtn = document.getElementById('logoutBtn');
        this.usersList = document.getElementById('usersList');
        this.messagesContainer = document.getElementById('messagesContainer');
        this.messageForm = document.getElementById('messageForm');
        this.messageInput = document.getElementById('messageInput');
        
        // Loading overlay
        this.loadingOverlay = document.getElementById('loadingOverlay');
    }

    bindEvents() {
        // Login form submission
        this.loginForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.handleLogin();
        });

        // Message form submission
        this.messageForm.addEventListener('submit', (e) => {
            e.preventDefault();
            this.sendMessage();
        });

        // Logout button
        this.logoutBtn.addEventListener('click', () => {
            this.handleLogout();
        });

        // Enter key in message input
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
    }

    connectSocket() {
        this.showLoading();
        
        // Connect to Socket.IO server
        this.socket = io();
        
        this.socket.on('connect', () => {
            console.log('Connected to server');
            this.hideLoading();
        });

        this.socket.on('disconnect', () => {
            console.log('Disconnected from server');
            this.showNotification('Connection lost. Trying to reconnect...', 'error');
        });

        this.socket.on('connect_error', (error) => {
            console.error('Connection error:', error);
            this.hideLoading();
            this.showNotification('Failed to connect to server', 'error');
        });

        // Handle real-time events
        this.socket.on('user_joined', (data) => {
            this.handleUserJoined(data);
        });

        this.socket.on('user_left', (data) => {
            this.handleUserLeft(data);
        });

        this.socket.on('update_user_list', (data) => {
            this.updateUsersList(data.users);
        });

        this.socket.on('new_message', (data) => {
            this.addMessage(data);
        });
    }

    async handleLogin() {
        const username = this.usernameInput.value.trim();
        
        if (!username) {
            this.showNotification('Please enter a username', 'error');
            return;
        }

        this.showLoading();

        try {
            const response = await fetch('/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username })
            });

            const data = await response.json();

            if (data.success) {
                this.currentUser = username;
                this.users = data.users;
                this.showChatScreen();
                this.updateUsersList(data.users);
                this.socket.emit('join', { username });
                this.showNotification(`Welcome, ${username}!`, 'success');
            } else {
                this.showNotification(data.message, 'error');
            }
        } catch (error) {
            console.error('Login error:', error);
            this.showNotification('Failed to login. Please try again.', 'error');
        } finally {
            this.hideLoading();
        }
    }

    async handleLogout() {
        if (!this.currentUser) return;

        try {
            await fetch('/logout', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username: this.currentUser })
            });

            this.socket.emit('leave', { username: this.currentUser });
            this.currentUser = null;
            this.users = [];
            this.messages = [];
            this.showLoginScreen();
            this.showNotification('Logged out successfully', 'success');
        } catch (error) {
            console.error('Logout error:', error);
            this.showNotification('Failed to logout', 'error');
        }
    }

    sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message || !this.currentUser) return;

        this.socket.emit('send_message', {
            username: this.currentUser,
            message: message
        });

        this.messageInput.value = '';
    }

    handleUserJoined(data) {
        if (data.username !== this.currentUser) {
            this.showNotification(`${data.username} joined the chat`, 'info');
        }
    }

    handleUserLeft(data) {
        if (data.username !== this.currentUser) {
            this.showNotification(`${data.username} left the chat`, 'info');
        }
    }

    updateUsersList(users) {
        this.users = users;
        this.usersList.innerHTML = '';
        
        users.forEach(username => {
            const userItem = document.createElement('div');
            userItem.className = 'user-item';
            userItem.innerHTML = `
                <i class="fas fa-circle" style="color: #28a745; margin-right: 8px;"></i>
                ${username}
            `;
            this.usersList.appendChild(userItem);
        });
    }

    addMessage(data) {
        const message = {
            username: data.username,
            message: data.message,
            timestamp: new Date(data.timestamp),
            isOwn: data.username === this.currentUser
        };

        this.messages.push(message);
        this.displayMessage(message);
        this.scrollToBottom();
    }

    displayMessage(message) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${message.isOwn ? 'own' : 'other'}`;
        
        const timeString = message.timestamp.toLocaleTimeString([], { 
            hour: '2-digit', 
            minute: '2-digit' 
        });

        messageElement.innerHTML = `
            <div class="message-content">
                <div class="message-header">
                    <span class="username">${message.username}</span>
                    <span class="timestamp">${timeString}</span>
                </div>
                <div class="message-text">${this.escapeHtml(message.message)}</div>
            </div>
        `;

        this.messagesContainer.appendChild(messageElement);
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    scrollToBottom() {
        this.messagesContainer.scrollTop = this.messagesContainer.scrollHeight;
    }

    showLoginScreen() {
        this.loginScreen.classList.add('active');
        this.chatScreen.classList.remove('active');
        this.usernameInput.value = '';
        this.usernameInput.focus();
    }

    showChatScreen() {
        this.loginScreen.classList.remove('active');
        this.chatScreen.classList.add('active');
        this.currentUserSpan.textContent = this.currentUser;
        this.messageInput.focus();
    }

    showLoading() {
        this.loadingOverlay.classList.remove('hidden');
    }

    hideLoading() {
        this.loadingOverlay.classList.add('hidden');
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }
}

// Initialize the app when the DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ChatApp();
});
