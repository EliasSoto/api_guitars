from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from sqlalchemy.orm import Session
from database.session import get_db
from core.auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter()

# Endpoint para la autenticación de usuarios.
@router.post("/token", tags=["Autenticación"], include_in_schema=False)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Credenciales incorrectas"
        )
    
    # Se genera el token de acceso con la información del usuario.
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={
            "first_name": user.first_name,
            "last_name": user.last_name,
            "user_id": user.id,  
            "role": "admin" if user.is_admin else "user",
            "rut": user.rut      
        },
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_info": { 
            "id": user.id,
            "fullname": f"{user.first_name} {user.last_name}",
            "rut": user.rut,
            "role": "admin" if user.is_admin else "user",
        }
    }
