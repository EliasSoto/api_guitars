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
from routers import guitar
from routers import order
from routers import shipment
from routers import custom_guitar
from routers import component
from routers import review
from routers import wishlist
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
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(login.router)
app.include_router(users.router)
app.include_router(address.router)
app.include_router(guitar.router)
app.include_router(order.router)
app.include_router(shipment.router)
app.include_router(custom_guitar.router)
app.include_router(component.router)
app.include_router(review.router)
app.include_router(wishlist.router)
