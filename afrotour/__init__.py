from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import os

db = SQLAlchemy()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Path for SQLite database
    base_dir = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(base_dir, 'afrotour')}"
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ECHO'] = True  # Enable SQL query logging
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

    db.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)

    # Enable CORS
    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

    # Register blueprints
    from afrotour.routes.auth import auth as auth_blueprint
    from afrotour.routes.tour import tour as tour_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
    app.register_blueprint(tour_blueprint, url_prefix='/api/tours')

    return app
