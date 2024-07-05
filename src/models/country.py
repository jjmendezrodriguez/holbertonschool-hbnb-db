"""
Country related functionality
"""

from src.models.base import Base
from . import db

class Country(Base):
    """
    Country representation

    This class does NOT inherit from Base, you can't delete or update a country

    This class is used to get and list countries
    """

    __tablename__ = 'countries'

    code = db.Column(db.String(3), primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    def __init__(self, name: str, code: str, **kw):
        """Init"""
        super().__init__(**kw)
        self.name = name
        self.code = code

    def __repr__(self) -> str:
        """Repr"""
        return f"<Country {self.code} ({self.name})>"

    def to_dict(self) -> dict:
        """Returns the dictionary representation of the country"""
        return {
            "name": self.name,
            "code": self.code,
        }

    @staticmethod
    def get_all() -> list["Country"]:
        """Get all countries"""
        from src.persistence.data_manager import DBRepository
        storege = DBRepository()
        return storege.get_all("country")

    @staticmethod
    def get(code: str) -> "Country | None":
        """Get a country by its code"""
        from src.persistence.data_manager import DBRepository
        storage = DBRepository()
        if storage.use_database:
            return Country.query.get(code)
        else:
            return storage.get("country", code)
    
    @staticmethod
    def create(data: dict) -> "Country":
        """Create a new country"""
        from src.persistence.data_manager import DBRepository
        storage = DBRepository()

        # Verificar si el país ya existe en la base de datos
        if storage.use_database:
            existing_country = Country.query.get(data["code"])
            if existing_country:
                raise ValueError(f"Country with code {data['code']} already exists")

        # Verificar si el país ya existe en el archivo JSON
        else:
            existing_country = storage.get("country", data["code"])
            if existing_country:
                raise ValueError(f"Country with code {data['code']} already exists")

        new_country = Country(name=data["name"], code=data["code"])
        storage.save(new_country) # si activo clona el country.
        return new_country

