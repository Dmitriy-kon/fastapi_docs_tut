from app.db import fake_items_db
from app.models.enum_models import ModelName

from fastapi import FastAPI

app = FastAPI(description="Some new message")


# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip: skip + limit]


@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None, short: bool = False):
    item = {"item_id": item_id}
    if q:
        item |= {"q": q}
    if not short:
        item |= {"description": "This is an amazing item that has a long description"}
    return item

@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item |= {"q": q}
    if not short:
        item |= {
            "description": "This is an amazing item that has a long description"
        }
    return item

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    return {"model_name": model_name, "message": "Hello"}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
