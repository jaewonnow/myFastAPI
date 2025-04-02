from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from app.api.routers import api_router  # routers.py에서 라우터 가져오기

app = FastAPI()

# 📌 템플릿 설정 (templates 폴더 사용)
templates = Jinja2Templates(directory="templates")

# 📌 라우터 등록
app.include_router(api_router)

@app.get('/test')
async def read_test(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})

@app.get('/')
async def read_root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get('/about')
async def read_about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})
