from app.schemas.schemas import UserCreate
from sqlalchemy.orm import Session
from app.models.models import User
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
