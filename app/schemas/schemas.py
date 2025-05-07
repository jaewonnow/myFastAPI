from pydantic import BaseModel,field_validator,EmailStr
from typing import Optional
from pydantic import  StringConstraints
from typing import Annotated

class UserCreate(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1, max_length=30)]
    username: Annotated[str, StringConstraints(min_length=3, max_length=20)]
    email: EmailStr
    user_id: Annotated[str, StringConstraints(min_length=4, max_length=20)]
    user_pw: Annotated[str, StringConstraints(min_length=8, max_length=100)]

    @field_validator("name", "username", "user_id", "user_pw", mode="before")
    @classmethod
    def not_blank(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("공백만으로 구성된 값은 사용할 수 없습니다.")
        return value

class UserLogin(BaseModel):
    user_id: str
    user_pw: str

class MemoCreate(BaseModel):
    title: str
    content: str

    @field_validator('title', 'content')
    def not_empty(cls, v, field):
        if not v.strip():
            raise ValueError(f"{field.name.capitalize()}는 비워둘 수 없습니다.")
        return v

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

