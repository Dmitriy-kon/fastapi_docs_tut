from typing import Annotated
from app.db import fake_items_db
from app.models.enum_models import ModelName, Models

from app.models import Item

from fastapi import Depends, FastAPI, Query

app = FastAPI(description="Some new message")


# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip: skip + limit]


@app.get("/items/")
async def read_items(q: Annotated[str | None, Query(max_length=10, pattern=r"^\D*sam\w*$")] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results |= {"q": q}
    return results


@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict |= {"price_with_tax": price_with_tax}

    return item_dict


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, q: str | None = None):
    res = {"item_id": item_id} | item.model_dump()
    if q:
        return res | {"q": q}
    return res


@app.get("/users/{user_id}/items/{item_id}")
async def read_user_item(
    user_id: int, item_id: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "owner_id": user_id}
    if q:
        item |= {"q": q}
    if not short:
        item |= {"description": "This is an amazing item that has a long description"}
    return item


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName, model: Annotated[Models, Depends()]):
    return {"model_name": model_name, "message": "Hello", "model": model}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}
