"""
Reviews controller module
"""

from flask import abort, request
from src.models.review import Review

def get_reviews():
    """Returns all reviews"""
    reviews = Review.get_all()
    return [review.to_dict() for review in reviews], 200

def create_review(place_id: str):
    """Creates a new review"""
    data = request.get_json()

    if "user_id" not in data:
        abort(400, "Missing field: user_id")

    try:
        review = Review.create(data | {"place_id": place_id})
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(400, str(e))

    return review.to_dict(), 201

def get_reviews_from_place(place_id: str):
    """Returns all reviews from a specific place"""
    reviews = Review.get_all()
    return [
        review.to_dict() for review in reviews if review.place_id == place_id
    ], 200

def get_reviews_from_user(user_id: str):
    """Returns all reviews from a specific user"""
    reviews = Review.get_all()
    return [
        review.to_dict() for review in reviews if review.user_id == user_id
    ], 200

def get_review_by_id(review_id: str):
    """Returns a review by ID"""
    review = Review.get(review_id)
    if not review:
        abort(404, f"Review with ID {review_id} not found")
    return review.to_dict(), 200

def update_review(review_id: str):
    """Updates a review by ID"""
    data = request.get_json()

    try:
        review = Review.update(review_id, data)
    except ValueError as e:
        abort(400, str(e))

    if not review:
        abort(404, f"Review with ID {review_id} not found")

    return review.to_dict(), 200

def delete_review(review_id: str):
    """Deletes a review by ID"""
    if not Review.delete(review_id):
        abort(404, f"Review with ID {review_id} not found")

    return "", 204
