from fastapi import APIRouter, Depends,Request
from sqlalchemy.orm import Session
from app.schemas.schemas import UserCreate
from app.crud.User_crud import create_user,get_mymemos
from app.db.db import get_db
from fastapi import Form
from app.models.models import User

router = APIRouter()
from app.core.security import get_current_user,get_current_user_optional
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

@router.get("/me")  # 또는 "/users/me"
def read_current_user(current_user: User = Depends(get_current_user)):
    return {
        "user_id": current_user.user_id,
        "name" : current_user.name,
        "username": current_user.username,
        "email": current_user.email,
        "user_id" : current_user.user_id,
        "user_pw" : current_user.user_pw
    }
    
@router.get("/memo") 
def read_current_user(current_user: User = Depends(get_current_user_optional)):
    
    return get_Mymemos(current_user)
    

@router.get("/mypage")
async def read_mypage(
    
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    return templates.TemplateResponse("mypage.html", {
        "request": request,
        "user": current_user
    })
    
    
# @router.post("/test-anon")
# async def test_anonymous(
#     current_user: Optional[User] = Depends(get_current_user_optional)
# ):
#     if current_user is None:
#         return {"message": "익명 사용자입니다."}
#     return {"message": f"안녕하세요, {current_user.username}님!"}