from flask import Blueprint, request, jsonify
from afrotour import db
from afrotour.models.user import User
from flask_jwt_extended import create_access_token

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Check if user already exists
    if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
        return jsonify({"message": "User already exists"}), 409

    # Create new user and add to the database
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity={'username': username, 'email': email})
    return jsonify({
        "message": "User registered successfully", "access_token": access_token
    }), 201

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        access_token = create_access_token(identity={'username': user.username, 'email': user.email})
        return jsonify({
            "message": "Login successful", "access_token": access_token
        }), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401
