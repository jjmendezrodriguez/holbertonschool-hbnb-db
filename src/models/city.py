"""
City related functionality
"""

from src.models.base import Base
from src.models.country import Country
from . import db

class City(Base):
    """City representation"""

    __tablename__ = 'cities'

    name = db.Column(db.String(128), nullable=False)
    country_code = db.Column(db.String(3), db.ForeignKey('countries.code'), nullable=False)

    def __init__(self, name: str, country_code: str, **kw) -> None:
        """Init"""
                   
        super().__init__(**kw)
        self.name = name
        self.country_code = country_code

    def __repr__(self) -> str:
        """Repr"""
        return f"<City {self.id} ({self.name})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "name": self.name,
            "country_code": self.country_code,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def create(data: dict) -> "City":
        """Create a new city"""
        from src.persistence import repo
        from src.models.country import Country

        # Verificar si el país existe
        country = Country.get(data["country_code"])
        if not country:
            raise ValueError("Country not found")

        # Verificar si la ciudad ya existe en el archivo JSON o la base de datos
        existing_city = City.query.filter_by(name=data["name"]).first()
        if existing_city:
            if existing_city.country_code == data["country_code"]:
                raise ValueError(f"City with name {data['name']} in country {data['country_code']} already exists")

        # Crear nueva ciudad
        city = City(**data)
        repo.save(city)

        return city

    @staticmethod
    def update(city_id: str, data: dict) -> "City":
        """Update an existing city"""
        from src.persistence import repo

        city = City.get(city_id)

        if not city:
            raise ValueError("City not found")

        for key, value in data.items():
            setattr(city, key, value)

        repo.update(city)

        return city
