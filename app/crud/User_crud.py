from app.schemas.schemas import UserCreate
from sqlalchemy.orm import Session
from app.models.models import User,Memo
from app.core.security import get_password_hash
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

def get_user(db: Session, user_id: str):
    return db.query(User).filter(User.user_id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_name(db: Session, name: str):
    return db.query(User).filter(User.name == name).first()

def get_mymemos(db: Session, current_user: User):
    return db.query(Memo).filter(Memo.user_id == current_user.id).all()