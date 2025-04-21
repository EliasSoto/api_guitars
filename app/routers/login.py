from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session
from database.session import get_db
from core.auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

#Endpoint para la autenticación de usuarios oculto (false)
@router.post("/token", tags=["Autenticación"], include_in_schema=False)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credenciales incorrectas"
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "sub": user.nombres,  # Cambiado de correo a nombres
            "user_id": user.id,   # Añadido ID
            "role": "admin" if user.es_administrador else "user",
            "rut": user.rut      # Añadido RUT para referencia
        },
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_info": {  # Datos adicionales para el frontend
            "id": user.id,
            "nombres": user.nombres,
            "rut": user.rut
        }
    }
