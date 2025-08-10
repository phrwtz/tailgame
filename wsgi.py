#!/usr/bin/env python3
"""
WSGI entry point for production deployment
"""

import os
from app import app, socketio

if __name__ == "__main__":
    # Get configuration
    config = app.config
    
    # Set environment variables if not already set
    if not os.environ.get('FLASK_ENV'):
        os.environ['FLASK_ENV'] = 'production'
    
    # Run the application
    port = int(os.environ.get('PORT', config.get('PORT', 5001)))
    host = os.environ.get('HOST', config.get('HOST', '0.0.0.0'))
    
    print(f"🚀 Starting production server on {host}:{port}")
    socketio.run(app, host=host, port=port)
