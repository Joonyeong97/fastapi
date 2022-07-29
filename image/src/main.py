from typing import Union, Optional

from fastapi import FastAPI
from functions import *
from pydantic import BaseModel

app = FastAPI()


class Token(BaseModel):
    text: str
    test: Optional[str]


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/text/")
def read_item(text: Token):
    return {"tokenize": tokenize(text.text)}
