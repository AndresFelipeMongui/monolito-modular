import uuid
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import SECRET_KEY, ALGORITHM
from app.modules.auth.models import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")

        if not isinstance(sub, str) or not sub.strip():
            raise credentials_exception

        user_id = uuid.UUID(sub)
    except (JWTError, ValueError, TypeError):
        raise credentials_exception

    user: User | None = db.get(User, user_id)
    if user is None or not user.is_active:
        raise credentials_exception

    return user