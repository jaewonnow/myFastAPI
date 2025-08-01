from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

# Pydantic 모델 예시
class MemoResponse(BaseModel):
    id: int
    title: str
    content: str
    created_at: datetime # datetime 객체는 JSON으로 자동 직렬화됨

    model_config = ConfigDict(from_attributes=True) # SQLAlchemy 객체에서 Pydantic으로 변환 가능하게 함

class UserResponse(BaseModel):
    id: int
    name: str
    username: str
    email: str
    user_id: str # ORM 모델의 user_id
    memos: List[MemoResponse] = [] # UserResponse에 MemoResponse 리스트 포함

    model_config = ConfigDict(from_attributes=True) # SQLAlchemy 객체에서 Pydantic으로 변환 가능하게 함