"""Flask app factory."""

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import DevelopmentConfig
import os

db = SQLAlchemy()


def create_app(config_name: str = "development") -> Flask:
    """App factory."""
    # Setup folders
    app_dir = os.path.dirname(os.path.abspath(__file__))
    template_dir = os.path.join(app_dir, 'templates')
    static_dir = os.path.join(app_dir, 'static')
    
    app = Flask(__name__, template_folder=template_dir, static_folder=static_dir)
    
    # Load config
    app.config.from_object(DevelopmentConfig)
    
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