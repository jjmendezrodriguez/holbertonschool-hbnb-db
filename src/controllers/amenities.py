"""
Amenity controller module
"""

from flask import abort, request
from src.models.amenity import Amenity

def get_amenities():
    """Returns all amenities"""
    amenities = Amenity.get_all()
    return [amenity.to_dict() for amenity in amenities], 200

def create_amenity():
    """Creates a new amenity"""
    data = request.get_json()

    try:
        amenity = Amenity.create(data)
        amenity.save()
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(400, str(e))

    return amenity.to_dict(), 201

def get_amenity_by_id(amenity_id: str):
    """Returns an amenity by ID"""
    amenity = Amenity.get(amenity_id)
    if not amenity:
        abort(404, f"Amenity with ID {amenity_id} not found")
    return amenity.to_dict(), 200

def update_amenity(amenity_id: str):
    """Updates an amenity by ID"""
    data = request.get_json()

    updated_amenity = Amenity.update(amenity_id, data)
    if not updated_amenity:
        abort(404, f"Amenity with ID {amenity_id} not found")

    return updated_amenity.to_dict(), 200

def delete_amenity(amenity_id: str):
    """Deletes an amenity by ID"""
    if not Amenity.delete(amenity_id):
        abort(404, f"Amenity with ID {amenity_id} not found")

    return "", 204
