from typing import Optional
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone  
from .config import SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer
from app.db.db import get_db


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)  # aware datetime
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")  # 로그인 경로
security = HTTPBearer(auto_error=False)  # 토큰 없으면 에러 안냄, None 반환

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    from app.crud.User_crud import get_user
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(db, user_id)
    if user is None:
        raise credentials_exception
    return user



async def get_current_user_optional(
    token: Optional[str] = Depends(security),
    db: Session = Depends(get_db)
):
    if token is None:
        return None  # 토큰 없으면 익명 사용자 처리

    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
    except JWTError:
        return None
    from app.crud.User_crud import get_user
    user = get_user(db, user_id)
    return user