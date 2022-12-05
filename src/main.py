from typing import Union, Optional

from fastapi import FastAPI
from functions import *
from pydantic import BaseModel

app = FastAPI()
model_name = 'joon09/kor-naver-ner-name'

ner_model = Ner(model_name)

class Token(BaseModel):
    text: list


@app.get("/")
def read_root():
    return {"Hello": "World123123123456456"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/ner_test/")
def get_name(text: Token):
    return {"tokens": ner_model(text.text)}