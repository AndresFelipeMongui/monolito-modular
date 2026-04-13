import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import hash_password, verify_password, create_access_token
from app.modules.auth.models import User
from app.modules.auth.schemas import RegisterRequest, LoginResponse, UserResponse
from app.modules.auth.service import get_current_user

router = APIRouter(tags=["Auth"])

@router.post("/auth/register", response_model=UserResponse, status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="El correo ya está registrado")

    user = User(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/auth/login", response_model=LoginResponse)
def login(
        form: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db),
):
    user: User | None = db.query(User).filter(User.email == form.username).first()
    if not user or not verify_password(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos",
        )
    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "Bearer"}

@router.get("/users/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    return current_user


@router.get("/users/{user_id}", response_model=UserResponse)
def get_user(
        user_id: uuid.UUID,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user
