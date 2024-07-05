"""
City related functionality
"""

from src.models.country import Country
import uuid
# src/models/city.py

from src.models.base import Base
from . import db

class City(Base):
    """City representation"""

    __tablename__ = 'cities'

    name = db.Column(db.String(128), nullable=False)
    code = db.Column(db.String(3), db.ForeignKey('countries.code'), nullable=False)

    def __init__(self, name: str, code: str, **kwargs):
        """Init"""
        super().__init__(**kwargs)
        self.name = name
        self.code = code

    def __repr__(self) -> str:
        """Repr"""
        return f"<City {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "code": self.code,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def create(data: dict) -> "City":
        """Create a new city"""
        from src.persistence.data_manager import DBRepository
        storage = DBRepository()

        # Generar un ID si no se proporciona
        if 'id' not in data:
            data['id'] = str(uuid.uuid4())

        # Verificar si la ciudad ya existe en la base de datos
        if storage.use_database:
            existing_city = City.query.get(data["id"])
            if existing_city:
                raise ValueError(f"City with id {data['id']} already exists")

        # Verificar si la ciudad ya existe en el archivo JSON
        else:
            existing_city = storage.get("city", data["id"])
            if existing_city:
                raise ValueError(f"City with id {data['id']} already exists")

        new_city = City(name=data["name"], code=data["code"], id=data["id"])
        storage.save(new_city)
        return new_city
