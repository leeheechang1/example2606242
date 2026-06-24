from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def read_root():
    return {'message':'집에가고싶다'}

@app.get('/hello/')
def read_hello():
    return {'message':'Hello, FastAPI!'}

@app.get('/item/{item_id}')
def read_item(item_id: int) -> dict:
    return {'item_id': f'{item_id}번 입력되었습니다'}

@app.get('/userid/{userid}/password/{password}')
def read_user(userid: str, password: str):
    a = f'{userid}, {password}입력되었습니다'
    return {'사용자ID': a}

@app.get('/login/{user}')
def read_login(user:str) -> dict:
    if user == '사용자':
        return {'로그인':'로그인 성공'}
    else:
        return {'로그인':'로그인 실패'}
    

#query 매개변수

@app.get('/query/')
def read_query(item:str) -> dict:
    ret = f'{item}을 찾고 있습니다'
    return {'query' : ret}


from fastapi import Query
# list
@app.get('/items/')
def read_items(q: list[str] = Query([])):
    return {'q': q}


    
# pydantic 모델
from pydantic import BaseModel