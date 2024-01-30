from typing import Annotated

from pydantic import BaseModel

from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse, RedirectResponse
from fastapi.exceptions import RequestValidationError
from fastapi import Body, Cookie, Depends, FastAPI, File, HTTPException, Header, Path, Query, Response, UploadFile, status, Form, Request

from starlette.exceptions import HTTPException as StarletteHTTPException

from app.db import fake_items_db
from app.models.enum_models import ModelName, Models

from app.models import Item, UserBase, UserIn
from app.exceptions import UnicornException
from app.body_update import router as body_router
from app.depends import router as common_router


app = FastAPI(description="Some new message")
app.include_router(body_router)
app.include_router(common_router)


# @app.get("/items/")
# async def read_item(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip: skip + limit]

@app.exception_handler(UnicornException)
async def unicorn_exception_handler(request: Request, exc: UnicornException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something. There goes a rainbow..."}
    )

@app.get("/unicorn/{name}")
async def read_unicorn(name: str):
    if name == "yolo":
        raise UnicornException(name=name)
    return {"unicorn_name": name}

@app.post("/files/")
async def create_file(
    file: Annotated[bytes, File()],
    fileb: Annotated[UploadFile, File()],
    token: Annotated[str, Form()],
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }


@app.post("/uploadfile/")
async def create_upload_file(file: Annotated[UploadFile, File(description="A file read as UploadFile")]):
    return {"filename": file.filename, "file.content_type": file.content_type}

@app.get("/items/", status_code=status.HTTP_200_OK, tags=["items"])
async def read_items(x_token: Annotated[list[str], Header()] = None):
    return {"X-Token values": x_token}


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return PlainTextResponse(str(exc.detail), status_code=exc.status_code)

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return PlainTextResponse(str(exc), status_code=400)


# @app.get("/items/{item_id}", tags=["items"])
# async def read_item(item_id: int):
#     if item_id == 3:
#         raise HTTPException(status_code=418, detail="Item not found")
#     return {"item": item_id}

@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):  # noqa: F821
    return {"username": username, "password": password}


@app.get("/")
async def main():
    content = """
<body>
<form action="/files/" enctype="multipart/form-data" method="post">
<input name="files" type="file" multiple>
<input type="submit">
</form>
<form action="/uploadfile/" enctype="multipart/form-data" method="post">
<input name="file" type="file" multiple>
<input type="submit">
</form>
</body>
    """
    return HTMLResponse(content=content)
# @app.get("/items/{item_id}")
# async def read_items(
#     item_id: Annotated[int, Path(title="Id of the item to ger")],
#     q: Annotated[str | None, Query(alias="item-query", deprecated=True)] = None,
# ):
#     results = {"item_id": item_id}
#     if q:
#         results |= {"q": q}
#     return results




@app.post("/items/", response_model=Item, response_model_exclude_unset=True, tags=["items"], summary="Create an item", response_description="Create an item with all the information")
async def create_item(item: Item):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    """
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
