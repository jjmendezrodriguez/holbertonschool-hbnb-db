"""
Places controller module
"""

from flask import abort, request
from src.models.place import Place

def get_places():
    """Returns all places"""
    places = Place.get_all()
    return [place.to_dict() for place in places], 200

def create_place():
    """Creates a new place"""
    data = request.get_json()

    try:
        place = Place.create(data)
        place.save()
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(404, str(e))

    return place.to_dict(), 201

def get_place_by_id(place_id: str):
    """Returns a place by ID"""
    place = Place.get(place_id)
    if not place:
        abort(404, f"Place with ID {place_id} not found")
    return place.to_dict(), 200

def update_place(place_id: str):
    """Updates a place by ID"""
    data = request.get_json()

    try:
        place = Place.update(place_id, data)
    except ValueError as e:
        abort(400, str(e))

    if not place:
        abort(404, f"Place with ID {place_id} not found")

    return place.to_dict(), 200

def delete_place(place_id: str):
    """Deletes a place by ID"""
    if not Place.delete(place_id):
        abort(404, f"Place with ID {place_id} not found")

    return "", 204
