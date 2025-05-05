from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    username: str
    email: str
    user_id: str
    user_pw: str

class UserLogin(BaseModel):
    user_id: str
    user_pw: str

class MemoCreate(BaseModel):
    title: str
    content: str

class MemoUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

class MemoResponse(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True

class MemoDelete(BaseModel):
    message: str
    memo_id: int

