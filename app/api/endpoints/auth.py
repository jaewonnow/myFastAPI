# app/api/auth.py
from fastapi import APIRouter
from sqlalchemy.orm import Session
from app.db.db import get_db
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import create_access_token, verify_password
from app.crud.User_crud import get_user, get_user_by_email
from app.Service.emailService import send_reset_email
from fastapi import BackgroundTasks

router = APIRouter()
from fastapi import Form

@router.post("/login")
def login(
    user_id: str = Form(...),
    user_pw: str = Form(...),
    db: Session = Depends(get_db)
):
    user = get_user(db, user_id)

    if not user or not verify_password(user_pw, user.user_pw):
        print("비밀번호 불일치")
        raise HTTPException(status_code=400, detail="Invalid credentials")

    token = create_access_token({"sub": user.user_id})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/forgot-password")
async def forgot_password(
    background_tasks: BackgroundTasks,  # ✅ 기본값 없는 인자 먼저
    email: str = Form(...),
    db: Session = Depends(get_db)
):
    user = get_user_by_email(db, email)
    if not user:
        # 항상 성공처럼 응답 (보안상 이메일 존재 여부 노출 방지)
        return {"msg": "이메일이 전송되었습니다. 확인해주세요."}

    reset_token = create_access_token({"sub": user.user_id}, expires_minutes=15)
    background_tasks.add_task(send_reset_email, email, reset_token)
    return {"msg": "이메일이 전송되었습니다. 확인해주세요."}