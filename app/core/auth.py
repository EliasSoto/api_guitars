from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
import os
from dotenv import load_dotenv
from repositories import user_repo

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
    print(f"Token generado: {to_encode}")  # Depuración
    return jwt.encode(to_encode, SECRET_KEY_TOKEN, algorithm=ALGORITHM)

# Verificar el token JWT y extraer el payload (username y role)
def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY_TOKEN, algorithms=[ALGORITHM])
        username = payload.get("sub")  # El 'sub' representa al username
        role = payload.get("role")  # El 'role' que se incluye en el payload
        if username is None or role is None:
            raise JWTError()
        # print(f"Token verificado: {username}, {role}")  # Depuración
        return {"username": username, "role": role}  # Devuelves un diccionario con el usuario y su rol
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido o expirado")

# Funciones para manejo de contraseñas
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# Función para autenticar al usuario
def authenticate_user(db, username: str, password: str):
    user = user_repo.get_user_by_username(db, username=username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
