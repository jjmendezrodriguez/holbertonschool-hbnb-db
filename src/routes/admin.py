from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from src.models import db, Amenity, City, User

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/amenities', methods=['POST'])
@jwt_required()
def create_amenity():
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403

    data = request.get_json()
    new_amenity = Amenity(name=data['name'])
    db.session.add(new_amenity)
    db.session.commit()
    return jsonify(new_amenity.to_dict()), 201

@admin_bp.route('/amenities/<amenity_id>', methods=['DELETE'])
@jwt_required()
def delete_amenity(amenity_id):
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403

    amenity = Amenity.query.get_or_404(amenity_id)
    db.session.delete(amenity)
    db.session.commit()
    return '', 204

@admin_bp.route('/cities', methods=['POST'])
@jwt_required()
def create_city():
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403

    data = request.get_json()
    new_city = City(name=data['name'], country_code=data['country_code'])
    db.session.add(new_city)
    db.session.commit()
    return jsonify(new_city.to_dict()), 201

@admin_bp.route('/cities/<city_id>', methods=['DELETE'])
@jwt_required()
def delete_city(city_id):
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403

    city = City.query.get_or_404(city_id)
    db.session.delete(city)
    db.session.commit()
    return '', 204

@admin_bp.route('/users/<user_id>/role', methods=['PUT'])
@jwt_required()
def change_user_role(user_id):
    claims = get_jwt()
    if not claims.get('is_admin'):
        return jsonify({"msg": "Administration rights required"}), 403

    user = User.query.get_or_404(user_id)
    data = request.get_json()
    user.is_admin = data.get('is_admin', user.is_admin)
    db.session.commit()
    return jsonify(user.to_dict()), 200
