"""
Countries controller module
"""

from flask import request, abort
from src.models.city import City
from src.models.country import Country

def get_countries():
    """Returns all countries"""
    countries = Country.get_all()
    return [country.to_dict() for country in countries], 200

def create_country():
    """Creates a new city"""
    data = request.get_json()

    try:
        country = Country.create(data)
        #country.save()
    except KeyError as e:
        abort(400, f"Missing field: {e}")
    except ValueError as e:
        abort(400, str(e))

    return country.to_dict(), 201

def get_country_by_code(code: str):
    """Returns a country by code"""
    country = Country.get(code)
    if not country:
        abort(404, f"Country with ID {code} not found")
    return country.to_dict(), 200

def get_country_cities(code: str):
    """Returns all cities for a specific country by code"""
    country = Country.get(code)
    if not country:
        abort(404, f"Country with ID {code} not found")

    cities = City.get_all()
    country_cities = [city.to_dict() for city in cities if city.country_code == country.code]
    return country_cities, 200

def delete_country(code: str):
    """Deletes a country by code"""
    if not Country.delete(code):
        abort(404, f"Country with code {code} not found")

    return "", 204

def update_country(code: str):
    """Updates a country by code"""
    data = request.get_json()

    country = Country.get(code)
    if not country:
        abort(404, f"Country with code {code} not found")

    # Update the fields
    if "name" in data:
        country.name = data["name"]

    try:
        country.save()
    except ValueError as e:
        abort(400, str(e))

    return country.to_dict(), 200