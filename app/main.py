from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

from models import usuario
from database.base import Base
from database.session import engine


# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Crear la aplicación FastAPI
app = FastAPI(
    title="CRUD API",
    description="Esta API permite crear, leer, actualizar y eliminar usuarios."
)