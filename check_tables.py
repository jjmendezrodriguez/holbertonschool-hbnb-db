from src.models import db
engine = db.create_engine('sqlite:///instance/hbnb_dev.db')
inspector = db.inspect(engine)
print(inspector.get_table_names())
