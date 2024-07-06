from src.models.base import Base
from src.models import db
import uuid


class User(Base):
    """User representation"""

    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(128), nullable=False) 
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, onupdate=db.func.current_timestamp())

    def __init__(self, email: str, first_name: str, last_name: str, password: str, is_admin: bool = False, **kw):
        """Init"""
        super().__init__(**kw)
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.is_admin = is_admin

    def __repr__(self) -> str:
        """Repr"""
        return f"<User {self.id} ({self.email})>"

    def to_dict(self) -> dict:
        """Dictionary representation of the object"""
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "password": self.password,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    @staticmethod
    def create(data: dict) -> "User":
        """Create a new user"""
        from src.persistence import repo

        users = User.get_all()

        for u in users:
            if u.email == data["email"]:
                raise ValueError("User already exists")

        new_user = User(**data)

        repo.save(new_user)

        return new_user

    # @staticmethod
    # def get(user_id: str) -> "User | None":
    #     """Get a user by ID"""
    #     return User.query.get(user_id)
    
    # """@staticmethod
    # def get_all() -> list["User"]:
        
    #     return User.query.all()"""
    
    @staticmethod
    def update(user_id: str, data: dict) -> "User | None":
        """Update an existing user"""
        from src.persistence.data_manager import DBRepository

        user = User.get(user_id)
        storage = DBRepository()
        
        if not user:
            return None

        # Actualiza los campos específicos si están presentes en data
        if "email" in data:
            user.email = data["email"]
        if "first_name" in data:
            user.first_name = data["first_name"]
        if "last_name" in data:
            user.last_name = data["last_name"]

        # Actualiza dinámicamente todos los demás campos proporcionados en data
        for key, value in data.items():
            if key not in ["email", "first_name", "last_name"]:
                setattr(user, key, value)

        storage.save(user)

        return user

    # @staticmethod
    # def delete(user_id: str) -> bool:
    #     """Delete a user by ID"""
    #     user = User.get(user_id)
    #     if user:
    #         db.session.delete(user)
    #         db.session.commit()
    #         return True
    #     return False