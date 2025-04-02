from sqlalchemy import Column, Integer, String
from app.db.db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100))
    user_id = Column(String(50), unique=True, index=True)
    user_pw = Column(String(255), index=True)

class Memo(Base):
    __tablename__ = "memos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    content = Column(String(1000))
    user_id = Column(Integer, index=True)  # 외래 키지만 관계 없음
