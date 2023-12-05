from typing import Union
({SQL_ALCH_IMPORT})
from fastapi import FastAPI

app = FastAPI()
({SQL_ALCH_DB_CONTENT})

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}
