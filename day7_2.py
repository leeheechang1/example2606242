from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
import random
import datetime
from enum import Enum

app = FastAPI()

@app.get('/')
def read_root():
    return {
        'message': '키움 디지털 아카데미 4기에 오신 것을 환영합니다!',
        '학습_단계': [
            '1단계: 기본 GET 요청',
            '2단계: 경로 매개변수',
            '3단계: 쿼리 매개변수',
            '4단계: POST 요청과 모델',
            '5단계: 실전 프로젝트',
        ],
        'tip': '/docs 에서 API 문서를 확인해보세요!'
    }



@app.get('/hello/{name}')
def read_hello(name: str):
    greetings = ['안녕하세요','반갑습니다','좋은하루예요']
    return {
        'message': f'{random.choice(greetings)}, {name}님!',
        'today': str(datetime.date.today()),
        'lucky_number': random.randint(1, 100)
    }


class Subject(str, Enum):
    math = "수학"
    korean = "국어"
    english = "영어"
    science = "과학"
    history = "역사"

@app.get('/grade/{subject}/{score}')
def get_grade(subject: Subject,
              score: int = Path(..., ge=0, le=100, description="점수 (0-100)")):
    if score >= 90:
        grade, comment = "A+", "최고예요!"
    elif score >= 80:
        grade, comment = "A", "잘했어요!!"
    elif score >= 70:
        grade, comment = "B", "조금만 더 힘내요!"
    elif score >= 60:
        grade, comment = "C", "더 열심히 공부해요!"
    else:
        grade, comment = "F", "다시 도전해요!"
    return {
        '과목': subject.value,
        '점수': score,
        '등급': grade,
        '코멘트': comment
    }
