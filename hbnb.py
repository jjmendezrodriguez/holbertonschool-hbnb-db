from dotenv import load_dotenv
import os

load_dotenv()  # Carga las variables de entorno desde el archivo .env
""" Another way to run the app"""

from src import create_app

app = create_app()

if __name__ == "__main__":
    app.run()
