from sqlalchemy.orm import Session
from app.models.models import  Memo
from app.schemas.schemas import  MemoCreate, MemoUpdate
from app.core.security import get_current_user,get_current_user_optional
from typing import Optional
from app.models.models import User
from fastapi import Depends
from .. import models
from datetime import datetime,timezone

# 메모 CRUD
def create_memo(db: Session, memo: MemoCreate, current_user: Optional[User] = None):
    db_memo = Memo(
        title=memo.title,
        content=memo.content,
        user_id= current_user.id if current_user else None, # 👈 사용자 이름 저장
        created_at= datetime.now(timezone.utc) 
    )
    db.add(db_memo)
    db.commit()
    db.refresh(db_memo)
    return db_memo

def get_memo(db: Session, memo_id: int):
    return db.query(Memo).filter(Memo.id == memo_id).first()

def get_user_memos(db: Session, user_id: int):
    return db.query(Memo).filter(Memo.user_id == user_id).all()

def get_memo_by_create(db: Session, created_at: datetime):
    return db.query(Memo).filter(Memo.created_at == created_at).first()

def get_all_memos(db: Session):
    return db.query(Memo).all()

def update_memo(db: Session, memo_id: int, memo_update: MemoUpdate):
    db_memo = db.query(Memo).filter(Memo.id == memo_id).first()
    if db_memo:
        if memo_update.title:
            db_memo.title = memo_update.title
        if memo_update.content:
            db_memo.content = memo_update.content
        db.commit()
        db.refresh(db_memo)
    return db_memo

def delete_memo(db: Session, memo_id: int):
    db_memo = db.query(models.Memo).filter(models.Memo.id == memo_id).first()
    if not db_memo:
        return None
    db.delete(db_memo)
    db.commit()
    return {"message": "메모가 삭제되었습니다.", "memo_id": memo_id}

