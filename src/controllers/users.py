"""
Users controller module
"""

from flask import abort, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.user import User
import uuid

@jwt_required()
def get_users():
    """Returns all users"""
    users = User.get_all()
    return [user.to_dict() for user in users], 200

def create_user():
    """Creates a new user"""
    data = request.get_json()

    try:
        user = User.create(data)
        user.save()
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(400, str(e))

    if user is None:
        abort(400, "User already exists")

    return user.to_dict(), 201

@jwt_required()
def get_user_by_id(user_id: str):
    """Returns a user by ID"""
    user = User.get(user_id)

    if not user:
        abort(404, f"User with ID {user_id} not found")

    return user.to_dict(), 200

@jwt_required()
def update_user(user_id: str):
    """Updates a user by ID"""
    current_user_id = get_jwt_identity()
    current_user = User.get(current_user_id)
    if not current_user.is_admin and current_user.id != user_id:
        abort(403, "Admin access required to update other users")

    data = request.get_json()

    try:
        user = User.update(user_id, data)
    except ValueError as e:
        abort(400, str(e))

    if user is None:
        abort(404, f"User with ID {user_id} not found")

    return user.to_dict(), 200

@jwt_required()
def delete_user(user_id: str):
    """Deletes a user by ID"""
    current_user_id = get_jwt_identity()
    current_user = User.get(current_user_id)
    if not current_user.is_admin:
        abort(403, "Admin access required")

    if not User.delete(user_id):
        abort(404, f"User with ID {user_id} not found")

    return "", 204
