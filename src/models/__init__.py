from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def init_app(app):
    db.init_app(app)

# modelos para que Alembic los detecte
from .user import User
from .city import City
from .country import Country
from .amenity import Amenity
from .place import Place
from .review import Review
