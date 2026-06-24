from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],  # React 개발 서버만 허용(허용할 출처)

    allow_credentials=True,  #(인증정보 허용, 쿠키, jWT토큰 등등)

    allow_methods=["*"],     #허용할 HTTP메서드(get, post, patch, put, delete)

    allow_headers=["*"],     #허용할 http헤더(Content-Type, Authorization)

)



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


@app.post("/login/", response_class=HTMLResponse)
async def login(request: Request, userid: str = Form(), password: str = Form()):
    if userid != 'user':
        result = '로그인 실패'
    elif password != '1234':
        result = '비밀번호가 다릅니다'
    else:
        result = '로그인 성공'
    return templates.TemplateResponse(request, 'login.html', {'result': result})