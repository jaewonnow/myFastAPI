from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from app.api.routers import api_router,auth_router  # routers.py 라우터 가져오기
from app.db.db import Base, engine

app = FastAPI()

# 📌 템플릿 설정 (templates 폴더 사용)
templates = Jinja2Templates(directory="templates")

# 📌 라우터 등록
app.include_router(api_router)
app.include_router(auth_router)

Base.metadata.create_all(bind=engine)

# 정적 파일 등록
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/')
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get('/about')
async def read_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})

@app.get('/login')
async def read_about(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get('/users/signup')
async def read_about(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.get('/users/signupcomplete')
async def read_about(request: Request):
    return templates.TemplateResponse("signupcomplete.html", {"request": request})

@app.get('/forgot_password')
async def read_about(request: Request):
    return templates.TemplateResponse("forgot_password.html", {"request": request})


