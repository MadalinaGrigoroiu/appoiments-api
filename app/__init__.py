"""
Flask application factory.
Initializes and configures the Flask app with SQLAlchemy.
"""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import DevelopmentConfig
import os

# Initialize SQLAlchemy
db = SQLAlchemy()


def create_app(config_name: str = "development") -> Flask:
    """
    Application factory function.
    
    Args:
        config_name: Configuration environment name
        
    Returns:
        Configured Flask application instance
    """
    # Get the absolute path to the app directory
    app_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(app_dir, 'templates')
    static_dir = os.path.join(app_dir, 'static')
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    
    # Load configuration (always development)
    app.config.from_object(DevelopmentConfig)
    
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

    @app.route("/")
    def index():
        """Main index route for the API."""
        return render_template("index.html")
    
    @app.route("/clients-page")
    def clients_page():
        """Route for the clients page."""
        return render_template("clients.html")

    @app.route("/services-page")
    def services_page():
        """Route for the services page."""
        return render_template("service.html")
    
    @app.route("/appointments-page")
    def appointments_page():    
        """Route for the appointments page."""
        return render_template("appoiments.html") 

    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app