from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

todo_data = {
    1:{'id':1, 'contents':'아침먹기', 'done':True},
    2:{'id':2, 'contents':'점심먹기', 'done':False},
    3:{'id':3, 'contents':'저녁먹기', 'done':False}
}

#전체 조회
@app.get('/todolist/')
def get_todolist():
    return list(todo_data.values())

#특정 ID로 조회
@app.get('/todos/{id}')
def get_todo(id:int):
    return todo_data.get(id,{})

class Class_Todo(BaseModel):
    id:int
    contents:str
    done:bool

@app.post('/insert_todo/')
def insert_todo(todo:Class_Todo):
    todo_data[todo.id]= todo.model_dump()
    return todo_data[todo.id]

@app.patch('/update_todo/{id}')
def update_todo(id:int, is_done:bool):
    if id in todo_data:
        todo_data[id]['done'] = is_done
        return todo_data[id]
    else:
        return {'message': '해당 아이디가 존재하지 않습니다'}

#특정 데이터 삭제하기
@app.delete('/delete_todo/{id}')
def delete_todo(id:int):
    if id in todo_data:
        todo_data.pop(id, None)
        return {'message': '삭제되었습니다'}
    else:
        return {'message': '해당 아이디가 존재하지 않습니다'}
