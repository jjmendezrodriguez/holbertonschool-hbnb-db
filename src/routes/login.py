from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from src.models.user import User
from werkzeug.security import check_password_hash

login_bp = Blueprint("login", __name__, url_prefix="/login")

@login_bp.route('/', methods=['POST'])
def login():
    data = request.get_json()
    print(f"Received data: {data}")
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        print("Missing email or password")
        return jsonify({"msg": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()
    print(f"Queried user: {user}")

    if not user or not check_password_hash(user.password_hash, password):
        print("Bad email or password")
        return jsonify({"msg": "Bad email or password"}), 401

    additional_claims = {"is_admin": user.is_admin}
    access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
    print(f"Issued access token: {access_token}")
    return jsonify(access_token=access_token), 200

@login_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify(logged_in_as=current_user_id), 200
