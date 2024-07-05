from flask import Flask, jsonify, render_template
from flask_cors import CORS
from src.models import db
import os
from sqlalchemy_utils import database_exists, create_database
import subprocess

cors = CORS()

def create_app(config_class=None) -> Flask:
    """
    Create a Flask app with the given configuration class.
    """
    app = Flask(__name__, template_folder='templates', static_folder='static')
    db_url = os.environ.get("DATABASE_URL")
    app.url_map.strict_slashes = False

    db_engine = db.create_engine(db_url)
    if not database_exists(db_engine.url):
        create_database(db_engine.url)
            
    if config_class is None:
        env = os.environ.get('ENV')
        if env == 'production':
            config_class = 'src.config.ProductionConfig'
        elif env == 'testing':
            config_class = 'src.config.TestingConfig'
        else:
            config_class = 'src.config.DevelopmentConfig'

    app.config.from_object(config_class)

    register_routes(app)
    register_extensions(app)
    register_handlers(app)
    pre_load(app)

    return app

def register_extensions(app: Flask) -> None:
    """Register the extensions for the Flask app"""
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Asegúrate de crear todas las tablas
    # Further extensions can be added here

def register_routes(app: Flask) -> None:
    """Import and register the routes for the Flask app"""
    from src.routes.users import users_bp
    from src.routes.countries import countries_bp
    from src.routes.cities import cities_bp
    from src.routes.places import places_bp
    from src.routes.amenities import amenities_bp
    from src.routes.reviews import reviews_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(countries_bp)
    app.register_blueprint(cities_bp)
    app.register_blueprint(places_bp)
    app.register_blueprint(reviews_bp)
    app.register_blueprint(amenities_bp)
    
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/toggle-persistence', methods=['POST'])
    def toggle_persistence():
        result = subprocess.run(['./switch_env.sh'], capture_output=True, text=True)
        if result.returncode == 0:
            return jsonify({"message": result.stdout.strip()})
        else:
            return jsonify({"message": "Error: " + result.stderr.strip()}), 500

    @app.route('/get-persistence-mode', methods=['GET'])
    def get_persistence_mode():
        use_database = os.getenv('USE_DATABASE', 'True').lower() in ('true', '1', 't')
        mode = 'db' if use_database else 'json'
        return jsonify({"mode": mode})

def register_handlers(app: Flask) -> None:
    """Register the error handlers for the Flask app."""
    app.errorhandler(404)(lambda e: (
        {"error": "Not found", "message": str(e)}, 404
    ))
    app.errorhandler(400)(lambda e: (
        {"error": "Bad request", "message": str(e)}, 400
    ))

def pre_load(app):
    from src.persistence.data_manager import DBRepository
    storage = DBRepository()
    with app.app_context():
        storage.reload()
