from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit, join_room, leave_room
import json
import os
from datetime import datetime
from config import get_config

app = Flask(__name__)
app.config.from_object(get_config())
socketio = SocketIO(app, cors_allowed_origins="*")

# Store active users and their sessions
active_users = {}
user_sessions = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username', '').strip()
    
    if not username:
        return jsonify({'success': False, 'message': 'Username is required'}), 400
    
    if username in active_users:
        return jsonify({'success': False, 'message': 'Username already taken'}), 400
    
    # Add user to active users
    active_users[username] = {
        'username': username,
        'joined_at': datetime.now().isoformat(),
        'status': 'online'
    }
    
    # Notify all clients about new user
    socketio.emit('user_joined', {
        'username': username,
        'joined_at': active_users[username]['joined_at']
    })
    
    # Send updated user list to all clients
    socketio.emit('update_user_list', {
        'users': list(active_users.keys())
    })
    
    return jsonify({
        'success': True, 
        'username': username,
        'users': list(active_users.keys())
    })

@app.route('/logout', methods=['POST'])
def logout():
    data = request.get_json()
    username = data.get('username', '')
    
    if username in active_users:
        del active_users[username]
        
        # Notify all clients about user leaving
        socketio.emit('user_left', {
            'username': username
        })
        
        # Send updated user list to all clients
        socketio.emit('update_user_list', {
            'users': list(active_users.keys())
        })
        
        return jsonify({'success': True})
    
    return jsonify({'success': False, 'message': 'User not found'}), 404

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

@socketio.on('join')
def handle_join(data):
    username = data.get('username')
    if username:
        join_room(username)
        print(f'User {username} joined room')

@socketio.on('leave')
def handle_leave(data):
    username = data.get('username')
    if username:
        leave_room(username)
        print(f'User {username} left room')

@socketio.on('send_message')
def handle_message(data):
    username = data.get('username')
    message = data.get('message')
    
    if username and message and username in active_users:
        # Broadcast message to all connected clients
        socketio.emit('new_message', {
            'username': username,
            'message': message,
            'timestamp': datetime.now().isoformat()
        })

if __name__ == '__main__':
    config = get_config()
    print("🚀 Starting Flask server...")
    print(f"🌐 Server will be available at: http://localhost:{config.PORT}")
    print("📱 Open multiple browser tabs to test with different users")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 50)
    socketio.run(app, debug=config.DEBUG, host=config.HOST, port=config.PORT)
