"""
Flask application factory.
Initializes and configures the Flask app with SQLAlchemy.
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import DevelopmentConfig, TestingConfig, ProductionConfig

# Initialize SQLAlchemy
db = SQLAlchemy()

# Configuration mapping
config_map = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}


def create_app(config_name: str = "development") -> Flask:
    """
    Application factory function.
    
    Args:
        config_name: Configuration environment name
        
    Returns:
        Configured Flask application instance
    """
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config_map.get(config_name, DevelopmentConfig))
    
    # Enable CORS
    CORS(app)
    
    # Initialize database
    db.init_app(app)
    
    # Register blueprints (routes)
    from app.routes import health, client_routes, service_routes, appointment_routes
    
    app.register_blueprint(health.bp)
    app.register_blueprint(client_routes.bp)
    app.register_blueprint(service_routes.bp)
    app.register_blueprint(appointment_routes.bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app