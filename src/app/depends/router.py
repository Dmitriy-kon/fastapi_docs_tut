from typing import Annotated
from fastapi import APIRouter, Depends


router = APIRouter(tags=["depends"])


async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


@router.get("/common-items")
async def read_items(commons: Annotated[dict, Depends(common_parameters)]):
    return commons


@router.get("/common-users")
async def read_users(commons: Annotated[dict, Depends(common_parameters)]):
    return commons
