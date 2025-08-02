from app.schemas.schemas import UserCreate
from sqlalchemy.orm import Session
from app.models.models import User,Memo
from app.core.security import get_password_hash
from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select
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

def get_user(db: Session, user_id: str, load_memos: bool = False):
    """
    주어진 user_id로 사용자 조회.
    load_memos가 True인 경우, 사용자의 메모 관계도 함께 로드합니다.
    """
    # 기본 쿼리: user_id를 기준으로 사용자를 조회
    statement = select(User).where(User.user_id == user_id)
    
    # load_memos 인자가 True인 경우, 즉시 로딩 옵션을 추가
    if load_memos:
        statement = statement.options(selectinload(User.memos))
        
    return db.execute(statement).scalar_one_or_none()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_name(db: Session, name: str):
    return db.query(User).filter(User.name == name).first()

def get_mymemos(db: Session, current_user: User):
    return db.query(Memo).filter(Memo.user_id == current_user.id).all()