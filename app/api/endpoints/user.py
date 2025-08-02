from fastapi import APIRouter, Depends,Request
from sqlalchemy.orm import Session
from app.schemas.schemas import UserCreate
from app.crud.User_crud import create_user,get_mymemos
from app.db.db import get_db
from fastapi import Form
from app.models.models import User
from app.models.PydanticModel import UserResponse

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

@router.get("/me", response_model=UserResponse) # response_model 추가
def read_current_user(current_user: User = Depends(get_current_user)):
    # current_user 객체에는 이미 memos 데이터가 로드되어 있습니다 (Eager Loading).
    # FastAPI는 UserResponse Pydantic 모델에 따라 current_user 객체를 직렬화합니다.
    # UserResponse 모델에 정의된 필드만 반환됩니다 (user_pw는 포함되지 않음).
    return current_user

# mypage.html을 렌더링하는 부분은 변경 없이 그대로 둡니다.
# (HTML 템플릿에서는 current_user 객체의 memos 속성을 직접 활용하면 됩니다.)
@router.get("/mypage")
async def read_mypage(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_optional)
):
    return templates.TemplateResponse("mypage.html", {
        "request": request,
        "user": current_user # current_user.memos를 템플릿에서 사용 가능
    })
    
# @router.post("/test-anon")
# async def test_anonymous(
#     current_user: Optional[User] = Depends(get_current_user_optional)
# ):
#     if current_user is None:
#         return {"message": "익명 사용자입니다."}
#     return {"message": f"안녕하세요, {current_user.username}님!"}