from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from afrotour.models.user import User

def admin_required_helper(fn):
    @wraps(fn)
    @jwt_required()  # Requires user to be logged in
    def wrapper(*args, **kwargs):
        identity = get_jwt_identity()
        user = User.query.filter_by(email=identity['email']).first()
        if user and user.is_admin:
            return fn(*args, **kwargs)
        return jsonify({"message": "Admin access required"}), 403
    return wrapper
