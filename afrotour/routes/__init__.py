from flask import Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  
from afrotour.models import User
from afrotour.models import Tour

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///afrotour.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)

    from afrotour.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
