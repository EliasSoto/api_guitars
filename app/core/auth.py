from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import os
from dotenv import load_dotenv
from repositories import user_repo
from models.usuario import Usuario  # Importar el modelo User desde el módulo correspondiente
from pydantic import BaseModel  # Importar BaseModel para definir TokenData

# Cargar variables de entorno
load_dotenv()

# Configuración de claves y algoritmo
SECRET_KEY_TOKEN = os.getenv("SECRET_KEY_TOKEN")  # Clave secreta del .env
ALGORITHM = os.getenv("ALGORITHM")  # Algoritmo de firma (por ejemplo: HS256)
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))  # Expiración del token (30 mins por defecto)

# Configuración de OAuth2 (Bearer Token)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Seguridad para contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Crear token JWT
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})  # Agregar la fecha de expiración al token
    return jwt.encode(to_encode, SECRET_KEY_TOKEN, algorithm=ALGORITHM)

# Verificar el token JWT y extraer el payload (username y role)
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY_TOKEN, algorithms=[ALGORITHM])
        nombres = payload.get("sub")
        user_id = payload.get("user_id")
        role = payload.get("role")
        rut = payload.get("rut")
        
        if None in [nombres, user_id, role, rut]:
            raise JWTError("Faltan campos requeridos en el token")
            
        return {
            "id": user_id,
            "username": nombres,
            "role": role,
            "rut": rut
        }
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
# Funciones para manejo de contraseñas
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Función para autenticar al usuario
def authenticate_user(db, nombres: str, hashed_password: str):
    user = user_repo.get_user_by_nombres(db, nombres=nombres)
    if not user:
        return None
    if not verify_password(hashed_password, user.hashed_password):
        return None
    return user
