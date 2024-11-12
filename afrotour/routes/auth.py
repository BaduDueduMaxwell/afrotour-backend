from flask import Blueprint, request, jsonify
from afrotour import db
from afrotour.models.user import User
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required
)
import os


auth = Blueprint('auth', __name__)


# Helper function for validating input
def validate_user_data(data):
    if not data.get('username'):
        return "Username is required", 400
    if not data.get('email'):
        return "Email is required", 400
    if not data.get('password'):
        return "Password is required", 400
    return None


# Register route
@auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    error_message = validate_user_data(data)
    if error_message:
        return jsonify({"error": error_message[0]}), error_message[1]

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

    access_token = create_access_token(user_identity={'id': new_user.id, 'username': username, 'email': email})
    refresh_token = create_refresh_token(user_identity={'id': new_user.id, 'username': username, 'email': email})
    
    return jsonify({
        "message": "User registered successfully",
        "access_token": access_token,
        "refresh_token": refresh_token
    }), 201


# Login route
@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"message": "Username and password are required"}), 400

    user = User.query.filter_by(username=username).first()
    if user and user.verify_password(password):
        access_token = create_access_token(user_identity={'id': user.id, 'username': user.username, 'email': user.email})
        refresh_token = create_refresh_token(user_identity={'id': user.id, 'username': user.username, 'email': user.email})
        
        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token
        }), 200
    else:
        return jsonify({"message": "Invalid username or password"}), 401


# Refresh token route
@auth.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    user_identity = get_jwt_identity()
    new_access_token = create_access_token(user_identity=user_identity)
    return jsonify(access_token=new_access_token), 200


# Update profile route
@auth.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_identity = get_jwt_identity()
    user = User.query.get_or_404(user_identity['id'])
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    # Only update fields that were provided
    if username:
        user.username = username
    if password:
        user.password_hash = generate_password_hash(password)
    if email:
        user.email = email
    
    # Commit changes to the database
    db.session.commit()

    return jsonify({
        "message": "Profile updated successfully",
        "user": user.to_dict()
    }), 200
