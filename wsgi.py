#!/usr/bin/env python3
"""
WSGI entry point for production deployment
"""

import os

# Set environment variables for production
os.environ['FLASK_ENV'] = 'production'

# Import app after setting environment
from app import app, socketio

if __name__ == "__main__":
    # Get port from environment (Render sets this automatically)
    port = int(os.environ.get('PORT', 5001))
    host = os.environ.get('HOST', '0.0.0.0')
    
    print(f"🚀 Starting production server on {host}:{port}")
    socketio.run(app, host=host, port=port)
