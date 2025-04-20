from jose import JWTError, jwt
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
from repositories import user_repo

load_dotenv()

# Configuración de claves y algoritmo
SECRET_KEY_TOKEN = os.getenv("SECRET_KEY_TOKEN")  # <- corregido aquí
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

# Seguridad para contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Soporte para Swagger UI (token por header Authorization: Bearer)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Crear token JWT
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    
    # Agregar el 'role' al token, usando el rol del usuario
    to_encode.update({"role": data.get("role")})

    return jwt.encode(to_encode, SECRET_KEY_TOKEN, algorithm=ALGORITHM)

# Verificar token JWT (retorna el "sub" (username) y "role" del payload)
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY_TOKEN, algorithms=[ALGORITHM])
        username = payload.get("sub")
        role = payload.get("role")  # Obtener el rol desde el payload
        if username is None or role is None:
            raise JWTError()
        return {"username": username, "role": role}  # Devuelves un diccionario con el usuario y su rol
    except JWTError:
        return None

# Hashing y verificación de contraseña
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Verifica credenciales y existencia del usuario
def authenticate_user(db: Session, username: str, password: str):
    user = user_repo.get_user_by_username(db, user_username=username)
    if not user:
        return None
    if not verify_password(password, user.password):
        return None
    return user
