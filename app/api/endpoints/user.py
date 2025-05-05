from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.schemas import UserCreate
from app.crud.User_crud import create_user
from app.db.db import get_db
from fastapi import Form
from app.models.models import User

router = APIRouter()
from app.core.security import get_current_user
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

@router.post("/signup")
async def signup(
    name: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),
    user_id: str = Form(...),
    user_pw: str = Form(...),
    db: Session = Depends(get_db)
):
    user = UserCreate(
        name=name,
        username=username,
        email=email,
        user_id=user_id,
        user_pw=user_pw
    )
    # 회원 생성 후 사용자 정보 JSON으로 반환
    return create_user(db, user)




router = APIRouter()

@router.get("/me")  # 또는 "/users/me"
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "user_id": current_user.user_id,
        "username": current_user.name,
    }