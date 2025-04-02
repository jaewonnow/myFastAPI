from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.schemas import MemoCreate, MemoUpdate
from app.crud.crud import create_memo, get_memo, update_memo, delete_memo
from app.db.db import get_db

router = APIRouter()

@router.post("/memos")
async def create_new_memo(memo: MemoCreate, db: Session = Depends(get_db)):
    return create_memo(db, memo)

@router.get("/memos/{memo_id}")
async def get_single_memo(memo_id: int, db: Session = Depends(get_db)):
    return get_memo(db, memo_id)

@router.put("/memos/{memo_id}")
async def update_existing_memo(memo_id: int, memo_update: MemoUpdate, db: Session = Depends(get_db)):
    return update_memo(db, memo_id, memo_update)

@router.delete("/memos/{memo_id}")
async def remove_memo(memo_id: int, db: Session = Depends(get_db)):
    return delete_memo(db, memo_id)
