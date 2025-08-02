from sqlalchemy import Column, Integer, String,DateTime,ForeignKey
from app.db.db import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)   
    name = Column(String(50))                               #실명
    username = Column(String(50), unique=True, index=True)  #닉네임
    email = Column(String(100))                             #이메일
    user_id = Column(String(50), unique=True, index=True)   #아이디
    user_pw = Column(String(255), index=True)               #비밀번호
    memos = relationship("Memo", back_populates="user")
    

class Memo(Base):
    __tablename__ = "memos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    content = Column(String(1000))
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="memos")
