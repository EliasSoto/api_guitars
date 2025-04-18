from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import os
from dotenv import load_dotenv

URL_DATABASE = os.getenv("URL_DATABASE")
# Crear el motor de conexión
engine = create_engine(URL_DATABASE)

# Crear la sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para usar en endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        db.rollback()
        print(f"Error al acceder a la base de datos: {e}")
    finally:
        db.close()
