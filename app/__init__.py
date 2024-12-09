from flask import Flask
from .db import db
from .routes import api_bp  # Import api_bp from routes.py
from .config import Config  # Import the Config class
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # Enable CORS for the app
    app.config.from_object(Config)  # Load configuration from the Config class
    
    db.init_app(app)
    app.register_blueprint(api_bp, url_prefix='/api')  # Register the blueprint with the app
    
    return app
