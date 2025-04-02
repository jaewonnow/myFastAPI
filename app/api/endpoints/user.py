from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.schemas import UserCreate
from app.crud.crud import create_user
from app.db.db import get_db

router = APIRouter()

@router.post("/signup")
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)
