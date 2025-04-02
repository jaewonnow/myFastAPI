from sqlalchemy.orm import Session
from app.models.models import User, Memo
from app.schemas.schemas import UserCreate, MemoCreate, MemoUpdate
from app.core.security import get_password_hash
from .. import models
# 유저 생성
def create_user(db: Session, user: UserCreate):
    hashed_pw = get_password_hash(user.user_pw)
    db_user = User(
        name=user.name, username=user.username, email=user.email, user_id=user.user_id, user_pw=hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 메모 CRUD
def create_memo(db: Session, memo: MemoCreate):
    db_memo = Memo(title=memo.title, content=memo.content)
    db.add(db_memo)
    db.commit()
    db.refresh(db_memo)
    return db_memo

def get_memo(db: Session, memo_id: int):
    return db.query(Memo).filter(Memo.id == memo_id).first()

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
