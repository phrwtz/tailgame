# Real-Time Chat Application

A modern, real-time chat application built with Python Flask backend and HTML/CSS/JavaScript frontend. Users can log in with a username and chat in real-time with other online users.

## Features

- **Real-time messaging**: Instant message delivery using WebSocket technology
- **User authentication**: Simple username-based login system
- **Live user list**: See all currently online users
- **Responsive design**: Works on desktop and mobile devices
- **Modern UI**: Beautiful gradient design with smooth animations
- **Real-time notifications**: Get notified when users join/leave
- **Message timestamps**: See when messages were sent
- **Auto-scroll**: Messages automatically scroll to the bottom

## Technology Stack

### Backend
- **Python 3.7+**
- **Flask**: Web framework
- **Flask-SocketIO**: WebSocket support for real-time communication
- **Eventlet**: Asynchronous networking library

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with gradients and animations
- **JavaScript (ES6+)**: Frontend logic and WebSocket handling
- **Socket.IO Client**: WebSocket client library
- **Font Awesome**: Icons

## Installation

1. **Clone the repository** (if applicable) or navigate to the project directory

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Start the server**:
   ```bash
   python app.py
   ```

2. **Open your browser** and navigate to:
   ```
   http://localhost:5001
   ```

3. **Enter a username** and click "Join Chat"

4. **Start chatting** with other users!

## How It Works

### Backend Architecture
- **Flask app**: Handles HTTP requests for login/logout
- **Socket.IO**: Manages real-time WebSocket connections
- **User management**: Tracks active users and their sessions
- **Message broadcasting**: Sends messages to all connected clients

### Frontend Architecture
- **Single Page Application**: Smooth transitions between login and chat screens
- **WebSocket connection**: Maintains real-time connection with server
- **Event-driven updates**: UI updates automatically based on server events
- **Responsive design**: Adapts to different screen sizes

### Real-time Features
- **User join/leave notifications**: Get notified when users come and go
- **Live user list**: See who's currently online
- **Instant messaging**: Messages appear immediately for all users
- **Connection status**: Visual feedback for connection issues

## API Endpoints

### HTTP Endpoints
- `POST /login`: User login with username
- `POST /logout`: User logout
- `GET /`: Main application page

### WebSocket Events
- `connect`: Client connects to server
- `disconnect`: Client disconnects from server
- `join`: User joins chat room
- `leave`: User leaves chat room
- `send_message`: User sends a message
- `user_joined`: New user joined notification
- `user_left`: User left notification
- `update_user_list`: Updated list of online users
- `new_message`: New message broadcast

## Customization

### Styling
- Modify `static/css/style.css` to change colors, fonts, and layout
- Update the gradient colors in the CSS variables
- Adjust responsive breakpoints for different screen sizes

### Functionality
- Add message persistence by implementing a database
- Implement user authentication with passwords
- Add private messaging capabilities
- Include file sharing features

## Troubleshooting

### Common Issues

1. **Port already in use**:
   - Change the port in `app.py` (line 95)
   - Kill processes using port 5001

2. **WebSocket connection failed**:
   - Check if the server is running
   - Verify firewall settings
   - Check browser console for errors

3. **Dependencies not found**:
   - Ensure virtual environment is activated
   - Run `pip install -r requirements.txt` again

### Debug Mode
The application runs in debug mode by default. For production:
- Set `debug=False` in `app.py`
- Use a production WSGI server like Gunicorn
- Configure proper logging

## Security Considerations

- **Input validation**: All user inputs are validated and sanitized
- **XSS protection**: HTML escaping prevents script injection
- **CSRF protection**: Consider adding CSRF tokens for production
- **Rate limiting**: Implement rate limiting for production use

## Performance

- **WebSocket efficiency**: Minimal overhead for real-time communication
- **Memory management**: Automatic cleanup of disconnected users
- **Scalability**: Can be extended with Redis for horizontal scaling

## Browser Support

- **Modern browsers**: Chrome, Firefox, Safari, Edge (latest versions)
- **Mobile browsers**: iOS Safari, Chrome Mobile
- **WebSocket support**: Required for real-time functionality

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application.

---

**Happy Chatting!** 🚀
