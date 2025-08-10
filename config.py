import os
from datetime import timedelta

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    DEBUG = False
    TESTING = False
    
    # Socket.IO configuration
    SOCKETIO_ASYNC_MODE = 'eventlet'
    SOCKETIO_PING_TIMEOUT = 60
    SOCKETIO_PING_INTERVAL = 25
    
    # CORS settings
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Server configuration
    HOST = os.environ.get('HOST', '0.0.0.0')
    PORT = int(os.environ.get('PORT', 5001))

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    SECRET_KEY = 'dev-secret-key'

class ProductionConfig(Config):
    """Production configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Production-specific settings
    SOCKETIO_ASYNC_MODE = 'eventlet'
    
    # Security headers
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SECRET_KEY = 'test-secret-key'

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config():
    """Get configuration based on environment"""
    config_name = os.environ.get('FLASK_ENV', 'default')
    return config[config_name]
