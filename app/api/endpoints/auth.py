# app/api/auth.py
from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.db.db import get_db

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token, verify_password
from app.crud.User_crud import get_user

router = APIRouter()
from fastapi import Form

@router.post("/login")
def login(
    user_id: str = Form(...),
    user_pw: str = Form(...),
    db: Session = Depends(get_db)
):
    user = get_user(db, user_id)
    print("입력된 사용자:", user_id)
    print("입력된 비밀번호:", user_pw)

    if not user or not verify_password(user_pw, user.user_pw):
        print("비밀번호 불일치")
        raise HTTPException(status_code=400, detail="Invalid credentials")

    print("로그인 성공")
    token = create_access_token({"sub": user.user_id})
    return {"access_token": token, "token_type": "bearer"}