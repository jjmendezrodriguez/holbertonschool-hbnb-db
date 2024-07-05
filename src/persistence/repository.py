""" Repository pattern for data access layer """

from abc import ABC, abstractmethod


class Repository(ABC):
    """Abstract class for repository pattern"""

    @abstractmethod
    def reload(self) -> None:
        """Reload data to the repository"""

    @abstractmethod
    def get_all(self, model_name: str) -> list:
        """Get all objects of a model"""

    @abstractmethod
    def get(self, model_name: str, id: str) -> None:
        """Get an object by id"""

    @abstractmethod
    def save(self, obj) -> None:
        """Save an object"""

    def update(self, obj):
        """Update an instance in the database or file system"""
        from src.models import db
        if self.use_database:
            db.session.add(obj)
            db.session.commit()  # Commit después de actualizar
            return obj
        else:
            return self._file_update(obj)


    @abstractmethod
    def delete(self, obj) -> bool:
        """Delete an object"""
