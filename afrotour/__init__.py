from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS  # Import CORS

db = SQLAlchemy()
jwt = JWTManager()  

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///afrotour.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'

    db.init_app(app)
    jwt.init_app(app)
    Migrate(app, db)

    # Enable CORS for the app
    CORS(app, origins=["http://localhost:5173/"])  # Allow specific origin

    # Import blueprints and register them after initializing CORS
    from afrotour.routes.auth import auth as auth_blueprint
    from afrotour.routes.tour import tour as tour_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/api/auth')
    app.register_blueprint(tour_blueprint, url_prefix='/api/tours')

    return app
