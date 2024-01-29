from typing import Annotated
from fastapi.params import Form

from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from app.db import fake_items_db
from app.models.enum_models import ModelName, Models

from app.models import Item, UserBase, UserIn

from fastapi import Body, Cookie, Depends, FastAPI, File, Header, Path, Query, Response, UploadFile, status

app = FastAPI(description="Some new message")


# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip: skip + limit]


@app.post("/files/")
async def create_file(file: Annotated[bytes, File()]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename, "file.content_type": file.content_type}

@app.get("/items/", status_code=status.HTTP_200_OK)
async def read_items(x_token: Annotated[list[str], Header()] = None):
    return {"X-Token values": x_token}

@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):  # noqa: F821
    return {"username": username, "password": password}


# @app.get("/items/{item_id}")
# async def read_items(
#     item_id: Annotated[int, Path(title="Id of the item to ger")],
#     q: Annotated[str | None, Query(alias="item-query", deprecated=True)] = None,
# ):
#     results = {"item_id": item_id}
#     if q:
#         results |= {"q": q}
#     return results


@app.get("/items2/")
async def read_itemss(
    q: Annotated[
        list[str], Query(title="Query list", description="add some query", min_length=3)
    ] = None,
):
    query_items = {"q": q}
    return query_items


@app.post("/items/", response_model=Item, response_model_exclude_unset=True)
async def create_item(item: Item):
    item_dict = item.model_dump()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict |= {"price_with_tax": price_with_tax}

    return item_dict


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


@app.post("/users/")
async def create_user(user: UserIn) -> UserBase:
    return user


@app.get("/models/{model_name}")
async def get_model(model_name: ModelName, model: Annotated[Models, Depends()]):
    return {"model_name": model_name, "message": "Hello", "model": model}


@app.get("/files/{file_path:path}")
async def read_file(file_path: str):
    return {"file_path": file_path}


@app.get("/teleport", response_model=None)
async def get_teleport(teleport: bool = False) -> Response | dict:
    if teleport:
        return RedirectResponse(url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    return {"message": "this is your interdimensional portal."}
