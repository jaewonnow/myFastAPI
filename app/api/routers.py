from fastapi import APIRouter
from app.api.endpoints import user, memo, auth  # 라우터 모듈 가져오기

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users", tags=["users"])
api_router.include_router(memo.router, prefix="/memos", tags=["memos"])

auth_router = APIRouter()
auth_router.include_router(auth.router, prefix="/auth", tags=["auth"])

#prefix="/users": 해당 라우터 안의 모든 엔드포인트가 /users 경로를 가지도록 지정
#tags=["users"]: Swagger UI 문서화 시 “users”라는 구분 섹션을 생성



