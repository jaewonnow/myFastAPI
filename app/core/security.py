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
    """
    현재 인증된 사용자를 즉시 로딩된 메모와 함께 가져옵니다.
    """
    # 순환 참조 문제를 해결하기 위해 함수 내부에 임포트
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
    except jwt.JWTError:
        raise credentials_exception

    # 여기서 즉시 로딩을 활성화합니다.
    user = get_user(db, user_id, load_memos=True)
    if user is None:
        raise credentials_exception
    return user



async def get_current_user_optional(
    token: Optional[str] = Depends(security),
    db: Session = Depends(get_db)
):
    from app.crud.User_crud import get_user
    if token is None:
        return None

    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
    except jwt.JWTError:
        return None

    # 여기서 즉시 로딩을 활성화합니다.
    user = get_user(db, user_id, load_memos=True)
    return user