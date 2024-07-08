from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models import db, Review, Place

protected_bp = Blueprint('protected', __name__, url_prefix='/protected')

@protected_bp.route('/places/<place_id>/reviews', methods=['POST'])
@jwt_required()
def submit_review(place_id):
    user_id = get_jwt_identity()
    data = request.get_json()
    new_review = Review(
        comment=data['comment'],
        rating=data['rating'],
        user_id=user_id,
        place_id=place_id
    )
    db.session.add(new_review)
    db.session.commit()
    return jsonify(new_review.to_dict()), 201

@protected_bp.route('/places/<place_id>/reviews/<review_id>', methods=['PUT'])
@jwt_required()
def edit_review(place_id, review_id):
    user_id = get_jwt_identity()
    review = Review.query.get_or_404(review_id)
    if review.user_id != user_id:
        return jsonify({"msg": "You can only edit your own reviews"}), 403

    data = request.get_json()
    review.comment = data['comment']
    review.rating = data['rating']
    db.session.commit()
    return jsonify(review.to_dict()), 200

@protected_bp.route('/places', methods=['POST'])
@jwt_required()
def create_place():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_place = Place(
        name=data['name'],
        description=data['description'],
        address=data['address'],
        latitude=data['latitude'],
        longitude=data['longitude'],
        host_id=user_id,
        city_id=data['city_id'],
        price_per_night=data['price_per_night'],
        number_of_rooms=data['number_of_rooms'],
        number_of_bathrooms=data['number_of_bathrooms'],
        max_guests=data['max_guests']
    )
    db.session.add(new_place)
    db.session.commit()
    return jsonify(new_place.to_dict()), 201

@protected_bp.route('/places/<place_id>', methods=['PUT'])
@jwt_required()
def update_place(place_id):
    user_id = get_jwt_identity()
    place = Place.query.get_or_404(place_id)
    if place.host_id != user_id:
        return jsonify({"msg": "You can only edit your own places"}), 403

    data = request.get_json()
    place.name = data['name']
    place.description = data['description']
    place.address = data['address']
    place.latitude = data['latitude']
    place.longitude = data['longitude']
    place.city_id = data['city_id']
    place.price_per_night = data['price_per_night']
    place.number_of_rooms = data['number_of_rooms']
    place.number_of_bathrooms = data['number_of_bathrooms']
    place.max_guests = data['max_guests']
    db.session.commit()
    return jsonify(place.to_dict()), 200

@protected_bp.route('/places/<place_id>', methods=['DELETE'])
@jwt_required()
def delete_place(place_id):
    user_id = get_jwt_identity()
    place = Place.query.get_or_404(place_id)
    if place.host_id != user_id:
        return jsonify({"msg": "You can only delete your own places"}), 403

    db.session.delete(place)
    db.session.commit()
    return '', 204
