from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.schemas import MemoCreate, MemoUpdate
from app.crud.Memo_crud import create_memo, get_memo, update_memo, delete_memo, get_all_memos
from app.db.db import get_db
from app.models.models import User
from app.core.security import get_current_user
router = APIRouter()

@router.post("/")
async def create_new_memo(
    memo: MemoCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return create_memo(db, memo, current_user)

@router.get("/all")
async def get_all_memos_view(db: Session = Depends(get_db)):
    return get_all_memos(db)

@router.get("/{memo_id}")
async def get_single_memo(memo_id: int, db: Session = Depends(get_db)):
    return get_memo(db, memo_id)

@router.put("/{memo_id}")
async def update_existing_memo(memo_id: int, memo_update: MemoUpdate, db: Session = Depends(get_db)):
    return update_memo(db, memo_id, memo_update)

@router.delete("/{memo_id}")
async def remove_memo(memo_id: int, db: Session = Depends(get_db)):
    return delete_memo(db, memo_id)
