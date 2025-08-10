#!/usr/bin/env python3
"""
WSGI entry point for production deployment
"""

import os

# Set environment variables for production
os.environ['FLASK_ENV'] = 'production'

# Import app after setting environment
from app import app

# For WSGI servers like Gunicorn
application = app

if __name__ == "__main__":
    # This file is primarily for WSGI servers
    # For direct execution, use app.py instead
    print("🚀 WSGI entry point loaded")
    print("📝 Use 'gunicorn wsgi:application' to run in production")
