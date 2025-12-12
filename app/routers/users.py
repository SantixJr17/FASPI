from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from ..crud import crud
from ..schemas import schemas
from ..security import security
from ..db.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Usuarios y Autenticación"],
)

@router.post(
    "/register/", 
    response_model=schemas.User,
    summary="Registrar nuevo usuario",
    description="Crea un nuevo usuario en el sistema con email y contraseña."
)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="El email ya está registrado")
    return crud.create_user(db=db, user=user)

@router.post(
    "/token", 
    response_model=schemas.Token,
    summary="Iniciar sesión",
    description="Autentica un usuario y retorna un token de acceso JWT para usar en endpoints protegidos."
)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                            db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get(
    "/me/", 
    response_model=schemas.User,
    summary="Obtener usuario actual",
    description="Retorna la información del usuario autenticado actualmente."
)
def read_users_me(current_user: schemas.User = Depends(security.get_current_user)):
    return current_user
