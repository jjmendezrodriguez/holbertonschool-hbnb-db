from src.persistence.repository import Repository
from src.models import db
import os
import json
from flask import current_app
from datetime import datetime

class DBRepository(Repository):
    """Database repository implementing the Repository (Storage) interface"""

    load_data = []

    def __init__(self) -> None:
        """Initialize the repository"""
        self.use_database = os.environ.get("USE_DATABASE")
        if self.use_database == "True":
            self.use_database = True
        else:
            self.use_database = False
        print(f"\n\nusing database: {(self.use_database)}") # check databse
        self.file_path = 'storage.json'
                
    def get_all(self, model_name: str) -> list:
        """Get all instances of a model"""
        from src.models.user import User
        from src.models.amenity import Amenity
        from src.models.city import City
        from src.models.place import Place
        from src.models.review import Review
        from src.models.country import Country
        if self.use_database:
            # Cargar datos desde la base de datos
            self.model_classes = {
            'user': User,
            'amenity': Amenity,
            'city': City,
            'place': Place,
            'review': Review,
            'country': Country
        }
            # model_name = "fake" (para probar mi codigo)
            if model_name in self.model_classes:
                model = self.model_classes[model_name]
                with current_app.app_context():
                    return model.query.all()
            else:
                print(f"\n\n \t-> -> fail loading model: {model_name}\n\n")
                return []
        else:
            return self._file_get_all(model_name)

    def get(self, model_name: str, obj_id: str):
        """Get a single instance of a model by ID"""
        from src.models.user import User
        from src.models.amenity import Amenity
        from src.models.city import City
        from src.models.place import Place
        from src.models.review import Review
        from src.models.country import Country
          # Cargar datos desde la base de datos
        self.model_classes = {
            'user': User,
            'amenity': Amenity,
            'city': City,
            'place': Place,
            'review': Review,
            'country': Country
        }
        if self.use_database:
            model = self.model_classes[model_name]
            return model.query.get(obj_id)
        else:
            return self._file_get(model_name, obj_id)
    
    def reload(self) -> None:
        """Reload the repository (if necessary)"""
        from src.models.user import User
        from src.models.amenity import Amenity
        from src.models.city import City
        from src.models.place import Place
        from src.models.review import Review
        from src.models.country import Country
        if self.use_database:
            # Cargar datos desde la base de datos
            self.model_classes = {
            'User': User,
            'Amenity': Amenity,
            'City': City,
            'Place': Place,
            'Review': Review,
            'Country': Country
        }
            with current_app.app_context():
                for model_name, model in self.model_classes.items():
                    instances = model.query.all()
                    for instance in instances:
                        DBRepository.load_data.append(instance)
                        
        else:
            # Cargar datos desde el archivo JSON
            data = self._load_data()
            for model_name, items in data.items():
                DBRepository.load_data.extend(items)  

    def save(self, obj) -> None:
        """Save an instance to the database or file system"""
        if self.use_database:
            db.session.add(obj)
            db.session.commit()  # Commit después de añadir
        else:
            self._file_save(obj)

    def update(self, obj):
        """Update an instance in the database or file system"""
        if self.use_database:
            db.session.commit()  # Commit después de actualizar
            return obj
        else:
            return self._file_update(obj)

    def delete(self, obj) -> bool:
        """Delete an instance from the database or file system"""
        if self.use_database:
            db.session.delete(obj)
            db.session.commit()  # Commit después de eliminar
            return True
        else:
            return self._file_delete(obj)

    def _file_get_all(self, model_name: str) -> list:
        """Get all instances of a model from the file"""
        try:
            with open(self.file_path, 'r') as f:
                data = json.load(f)
                return [self._dict_to_model(model_name, item) for item in data.get(model_name, [])]
        except FileNotFoundError:
            return []

    def _file_get(self, model_name: str, obj_id: str):
        """Get a single instance of a model by ID from the file"""
        instances = self._file_get_all(model_name)
        for instance in instances:
            if instance.id == obj_id or instance.code == obj_id:
                return instance
        return None

    def _file_save(self, obj) -> None:
        """Save an instance to the file"""
        data = self._load_data()
        model_name = obj.__class__.__name__.lower()
        if model_name not in data:
            data[model_name] = []

        obj_dict = obj.to_dict()
        if model_name == "country":
            # Si es un país, verifica si ya existe antes de añadirlo
            for item in data[model_name]:
                if item['code'] == obj_dict['code']:
                    raise ValueError(f"Country with code {obj_dict['code']} already exists")
        else:
            # Si no es un país, añade el objeto normalmente
            data[model_name].append(obj_dict)
        
        self._save_data(data)


    def _file_update(self, obj):
        """Update an instance in the file"""
        data = self._load_data()
        model_name = obj.__class__.__name__.lower()
        if model_name in data:
            for index, item in enumerate(data[model_name]):
                if item['id'] == obj.id:
                    data[model_name][index] = obj.to_dict()
                    self._save_data(data)
                    return obj
        return None

    def _file_delete(self, obj) -> bool:
        """Delete an instance from the file"""
        data = self._load_data()
        model_name = obj.__class__.__name__.lower()
        if model_name in data:
            if model_name == 'country':
                data[model_name] = [item for item in data[model_name] if item['code'] != obj.code]
            else:
                data[model_name] = [item for item in data[model_name] if item['id'] != obj.id]
            self._save_data(data)
            return True
        return False

    def _load_data(self) -> dict:
        """Load data from the file"""
        try:
            with open(self.file_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_data(self, data: dict) -> None:
        """Save data to the file"""
        with open(self.file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def _dict_to_model(self, model_name: str, data: dict):
        """Convert a dictionary to a model instance"""
        from src.models.user import User
        from src.models.amenity import Amenity
        from src.models.city import City
        from src.models.place import Place
        from src.models.review import Review
        from src.models.country import Country
        # Cargar datos desde la base de datos
        self.model_classes = {
            'user': User,
            'amenity': Amenity,
            'city': City,
            'place': Place,
            'review': Review,
            'country': Country
        }
        model = self.model_classes[model_name]
        # Asumir que las fechas están en formato ISO en el diccionario
        if 'created_at' in data:
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if 'updated_at' in data:
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        return model(**data)
