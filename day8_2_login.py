from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],  # React 개발 서버만 허용(허용할 출처)

    allow_credentials=True,  #(인증정보 허용, 쿠키, jWT토큰 등등)

    allow_methods=["*"],     #허용할 HTTP메서드(get, post, patch, put, delete)

    allow_headers=["*"],     #허용할 http헤더(Content-Type, Authorization)

)



USERID = 'user'
PASSWORD = '1234'


class Login(BaseModel):
    userid: str
    password: str


templates = Jinja2Templates(directory="templates")
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(
        request,
        'index.html',
        {'message': 'Hello world', 'name': 'LeeHeeChang'}
    )

@app.get("/login/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request, 'login.html')


@app.post("/login/")
async def login(login: Login):
    if login.userid != USERID:
        return {'message': '사용자 아이디가 다릅니다'}
    if login.password != PASSWORD:
        return {'message': '비밀번호가 다릅니다'}
    return {'message': '로그인 성공'}