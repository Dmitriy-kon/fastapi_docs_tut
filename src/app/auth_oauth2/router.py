from typing import Annotated


from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

router = APIRouter(tags=["auth"])

oauth2_sheme = OAuth2PasswordBearer(tokenUrl="token")


@router.get("/items-auth/")
async def read_items(token: Annotated[str, Depends(oauth2_sheme)]):
    return {"token": token}