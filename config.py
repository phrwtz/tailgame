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
    # Check for FLASK_ENV first (deprecated but still used by some platforms)
    config_name = os.environ.get('FLASK_ENV')
    
    # If FLASK_ENV is not set, check for other environment indicators
    if not config_name:
        if os.environ.get('RENDER') or os.environ.get('RAILWAY_ENVIRONMENT') or os.environ.get('HEROKU'):
            config_name = 'production'
        else:
            config_name = 'development'
    
    # Ensure config_name is valid
    if config_name not in config:
        config_name = 'default'
    
    # Debug logging
    print(f"🔧 Config: FLASK_ENV={os.environ.get('FLASK_ENV')}")
    print(f"🔧 Config: RENDER={os.environ.get('RENDER')}")
    print(f"🔧 Config: Selected config={config_name}")
    
    return config[config_name]
