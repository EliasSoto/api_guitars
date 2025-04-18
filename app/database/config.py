import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Leer la URL de la base de datos desde el archivo .env
DATABASE_URL = os.getenv("URL_DATABASE")
