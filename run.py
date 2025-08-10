#!/usr/bin/env python3
"""
Simple startup script for the Real-Time Chat Application
"""

import os
import sys
import subprocess

def check_dependencies():
    """Check if required packages are installed"""
    try:
        import flask
        import flask_socketio
        print("✓ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def main():
    print("🚀 Starting Real-Time Chat Application...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    print("✓ Dependencies check passed")
    print("✓ Starting Flask server...")
    print("\n🌐 The application will be available at: http://localhost:5001")
    print("📱 Open multiple browser tabs to test with different users")
    print("⏹️  Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Import and run the Flask app
        from app import app, socketio
        socketio.run(app, debug=True, host='0.0.0.0', port=5001)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
