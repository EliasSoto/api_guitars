#Importante para ejecutar el comando uvicorn app.main:app --reload 
#Sin hacer cd
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from database.base import Base
from database.session import engine
from routers import users
from routers import address
from routers import login
from fastapi.middleware.cors import CORSMiddleware

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Crear la aplicación FastAPI
app = FastAPI(
    title="API PROYECTO GUITARRAS",
    description="Esta API permite hacer CRUD por el momento"
)

app.add_middleware(
    CORSMiddleware,
<<<<<<< HEAD
    allow_origins=["*"],
=======
    allow_origins=["*"], 
>>>>>>> c3f4cf4eedc3eee8e5cfab6b5d370d45431cfb0f
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router)
app.include_router(users.router)
app.include_router(address.router)

#cerdo por ahora
