from logging.config import BaseConfigurator
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from starlette.requests import Request
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from starlette.status import HTTP_303_SEE_OTHER
from sqlalchemy.orm import sessionmaker, Session , mapped_column
from pydantic import BaseModel
from typing import Optional, List
from fastapi import Form
from passlib.context import CryptContext

# MySQL 연결 정보
DATABASE_URL = "mysql+pymysql://root:1219@localhost:3306/jmemo"

# SQLAlchemy 엔진 생성
engine = create_engine(DATABASE_URL, echo=True)

# 세션 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 선언
Base = declarative_base()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)  # 기본 키 설정
    name = Column(String(50))
    username = Column(String(50), unique=True, index=True)
    email = Column(String(100))
    user_id = Column(String(50), unique=True, index=True)
    user_pw = Column(String(255), index=True)

class UserCreate(BaseModel):
    
    name: str
    username: str
    email: str
    user_id: str
    user_pw: str

class UserLogin(BaseModel):
    user_id: str
    user_pw: str
    class Config (BaseConfigurator):
        orm_mode = True
    
class Memo(Base):
    __tablename__ = "memos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), index=True)
    content = Column(String(1000))
    user_id = Column(Integer, index=True)  # 외래 키지만 관계 없음
    
class MemoDelete(BaseModel):
    message: str
    memo_id: int

    class Config(BaseConfigurator):
        from_attributes = True

class MemoCreate(BaseModel):
    title: str
    content: str

class MemoUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None


class MemoResponse(BaseModel):
    id: int
    title: str
    content: str

    class Config(BaseConfigurator):
        from_attributes = True  # ORM 객체를 Pydantic 모델로 변환 가능하게 함

# ✅ 데이터베이스 초기화 함수
def init_db():
    Base.metadata.create_all(bind=engine)

# ✅ FastAPI 앱 생성
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# 의존성 주입: 데이터베이스 세션 가져오기
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
        
@app.get('/')
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get('/about')
async def read_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})




@app.get('/login')
async def read_login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login")
async def login(
        request: Request,
        userid: str = Form(...),
        password: str = Form(...),
        db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.user_id == userid).first()
    if not user or not verify_password(password, user.user_pw):  # 🔥 수정된 부분
        raise HTTPException(status_code=400, detail="Invalid username or password")

    response = RedirectResponse(url="/dashboard", status_code=HTTP_303_SEE_OTHER)
    return response


@app.post('/signup', response_class=HTMLResponse)
async def create_signup(
    request: Request,
    name: str = Form(...), 
    username: str = Form(...), 
    email: str = Form(...), 
    user_id: str = Form(...), 
    user_pw: str = Form(...), 
    db: Session = Depends(get_db)
):
    # 비밀번호 해싱 후 DB 저장
    hashed_pw = get_password_hash(user_pw)
    db_user = User(
        name=name, 
        username=username, 
        email=email, 
        user_id=user_id, 
        user_pw=hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # 🔥 회원가입 성공 페이지 반환
    return templates.TemplateResponse("registercomplete.html", {"request": request, "name": name})

@app.get('/signup')
async def read_signup(request: Request):
    # 회원가입 페이지를 렌더링
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get('/forgot_password')
async def get_forgot_password(request: Request):
    # 비밀번호 찾기 페이지를 렌더링
    return templates.TemplateResponse("forgot_password.html", {"request": request})

# # 1. 이름 검증
# @app.post("/validate_name")
# async def validate_name(name: str = Form(...)):
#     if len(name) < 2:
#         return JSONResponse(status_code=400, content={"error": "이름은 최소 2글자 이상이어야 합니다."})
#     if not name.isalpha():
#         return JSONResponse(status_code=400, content={"error": "이름은 문자만 포함해야 합니다."})
#     return JSONResponse(status_code=200, content={"message": "OK"})

# # 2. 이메일 검증
# @app.post("/validate_email")
# async def validate_email(email: str = Form(...), db: Session = Depends(get_db)):
#     email_regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
#     if not re.match(email_regex, email):
#         return JSONResponse(status_code=400, content={"error": "올바른 이메일 형식이 아닙니다."})
    
#     existing_user = db.query(User).filter(User.email == email).first()
#     if existing_user:
#         return JSONResponse(status_code=400, content={"error": "이미 존재하는 이메일입니다."})
    
#     return JSONResponse(status_code=200, content={"message": "OK"})

# # 3. 아이디 검증
# @app.post("/validate_id")
# async def validate_id(user_id: str = Form(...), db: Session = Depends(get_db)):
#     if len(user_id) < 5:
#         return JSONResponse(status_code=400, content={"error": "아이디는 최소 5글자 이상이어야 합니다."})
#     if not user_id.isalnum():
#         return JSONResponse(status_code=400, content={"error": "아이디는 영문과 숫자로만 구성되어야 합니다."})

#     existing_user = db.query(User).filter(User.id == user_id).first()
#     if existing_user:
#         return JSONResponse(status_code=400, content={"error": "이미 사용 중인 아이디입니다."})

#     return JSONResponse(status_code=200, content={"message": "OK"})

# # 4. 비밀번호 검증
# @app.post("/validate_password")
# async def validate_password(password: str = Form(...)):
#     if len(password) < 8:
#         return JSONResponse(status_code=400, content={"error": "비밀번호는 최소 8글자 이상이어야 합니다."})
    
#     if not re.search(r"[A-Z]", password):
#         return JSONResponse(status_code=400, content={"error": "비밀번호에는 최소 1개의 대문자가 포함되어야 합니다."})

#     if not re.search(r"[a-z]", password):
#         return JSONResponse(status_code=400, content={"error": "비밀번호에는 최소 1개의 소문자가 포함되어야 합니다."})

#     if not re.search(r"[0-9]", password):
#         return JSONResponse(status_code=400, content={"error": "비밀번호에는 최소 1개의 숫자가 포함되어야 합니다."})

#     if not re.search(r"[\W_]", password):
#         return JSONResponse(status_code=400, content={"error": "비밀번호에는 최소 1개의 특수문자가 포함되어야 합니다."})

#     return JSONResponse(status_code=200, content={"message": "OK"})


@app.get('/test')
async def read_test(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})







# ✅ 📌 메모 CRUD API 추가

## 📌 1️⃣ 모든 메모 조회 (GET /memos)
@app.get('/memos', response_model=List[MemoResponse])
async def get_memos(db: Session = Depends(get_db)):
    return db.query(Memo).all()

## 📌 2️⃣ 특정 메모 조회 (GET /memos/{memo_id})
@app.get('/memos/{memo_id}', response_model=MemoResponse)
async def get_memo(memo_id: int, db: Session = Depends(get_db)):
    memo = db.query(Memo).filter(Memo.id == memo_id).first()
    if not memo:
        raise HTTPException(status_code=404, detail="메모를 찾을 수 없습니다.")
    return memo

## 📌 3️⃣ 메모 추가 (POST /memos)
@app.post('/memos', response_model=MemoResponse)
async def create_memo(memo: MemoCreate, db: Session = Depends(get_db)):
    db_memo = Memo(title=memo.title, content=memo.content)
    db.add(db_memo)
    db.commit()
    db.refresh(db_memo)
    return db_memo

## 📌 4️⃣ 메모 수정 (PUT /memos/{memo_id})
@app.put('/memos/{memo_id}', response_model=MemoResponse)
async def update_memo(memo_id: int, memo_update: MemoUpdate, db: Session = Depends(get_db)):
    db_memo = db.query(Memo).filter(Memo.id == memo_id).first()
    if not db_memo:
        raise HTTPException(status_code=404, detail="메모를 찾을 수 없습니다.")
    
    if memo_update.title is not None:
        db_memo.title = memo_update.title
    if memo_update.content is not None:
        db_memo.content = memo_update.content
    
    db.commit()
    db.refresh(db_memo)
    return db_memo

## 📌 5️⃣ 메모 삭제 (DELETE /memos/{memo_id})
@app.delete('/memos/{memo_id}', response_model=MemoDelete)
async def delete_memo(memo_id: int, db: Session = Depends(get_db)):
    db_memo = db.query(Memo).filter(Memo.id == memo_id).first()
    if not db_memo:
        raise HTTPException(status_code=404, detail="메모를 찾을 수 없습니다.")

    db.delete(db_memo)
    db.commit()
    
    return MemoDelete(message="메모가 삭제되었습니다.", memo_id=memo_id)

# ✅ 서버 실행 전 데이터베이스 초기화
init_db()
