from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from models import usuario, direccion
from database.base import Base
from database.session import engine
from routers import users
from routers import login

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Crear la aplicación FastAPI
app = FastAPI(
    title="CRUD API",
    description="Esta API permite crear, leer, actualizar y eliminar usuarios."
)

app.include_router(login.router)
app.include_router(users.router)
