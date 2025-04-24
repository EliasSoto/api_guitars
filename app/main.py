from fastapi import FastAPI
from database.base import Base
from database.session import engine
from routers import users
from routers import address
from routers import login

# Crear las tablas en la base de datos
Base.metadata.create_all(bind=engine)

# Crear la aplicación FastAPI
app = FastAPI(
    title="API PROYECTO GUITARRAS",
    description="Esta API permite hacer CRUD por el momento"
)

app.include_router(login.router)
app.include_router(users.router)
app.include_router(address.router)

#cerdo


