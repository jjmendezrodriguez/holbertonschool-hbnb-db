from datetime import datetime
from typing import Any, Optional
import uuid
from abc import abstractmethod
from src.models import db
from sqlalchemy.ext.declarative import declarative_base

db_base = declarative_base()

class Base(db.Model):
    """
    Base Interface for all models
    """

    __abstract__ = True  # This makes SQLAlchemy understand this class should not be created as a table

    id = db.Column(db.String(36), primary_key=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(
        self,
        id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        **kwargs,
    ) -> None:
        """
        Base class constructor
        If kwargs are provided, set them as attributes
        """
        if kwargs:
            for key, value in kwargs.items():
                if hasattr(self, key):
                    continue
                setattr(self, key, value)

        self.id = str(id or uuid.uuid4())
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()

    @classmethod
    def get(cls, id) -> "Any | None":
        """
        This is a common method to get a specific object
        of a class by its id

        If a class needs a different implementation,
        it should override this method
        """
        from src.persistence.data_manager import DBRepository
        
        storage = DBRepository()

        return storage.get(cls.__name__.lower(), id)

    @classmethod
    def get_all(cls) -> list["Any"]:
        """
        This is a common method to get all objects of a class

        If a class needs a different implementation,
        it should override this method
        """
        from src.persistence.data_manager import DBRepository
        storage = DBRepository()

        return storage.get_all(cls.__name__.lower())

    # @classmethod
    # def delete(cls, id) -> bool:
        """
        This is a common method to delete a specific
        object of a class by its id

        If a class needs a different implementation,
        it should override this method
        
        from src.persistence import repo

        obj = cls.get(id)

        if not obj:
            return False

        return repo.delete(obj)"""
    
    @classmethod
    def delete(cls, id: str) -> bool:
        """Delete a user by ID"""
        from src.persistence.data_manager import DBRepository
        storage = DBRepository()
        obj = cls.get(id)
        if obj:
            storage.delete(obj)
            return True
        return False

    @abstractmethod
    def to_dict(self) -> dict:
        """Returns the dictionary representation of the object"""

    @staticmethod
    @abstractmethod
    def create(data: dict) -> Any:
        """Creates a new object of the class"""

    @staticmethod
    @abstractmethod
    def update(entity_id: str, data: dict) -> Any | None:
        """Updates an object of the class"""
        
    def save(self):
        from src.persistence.data_manager import DBRepository
        storage = DBRepository()
        storage.save(self)
        