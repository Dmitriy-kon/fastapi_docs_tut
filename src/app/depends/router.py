from typing import Annotated
from fastapi import APIRouter, Depends


router = APIRouter(tags=["depends"])


async def common_parameters(q: str = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}


CommonDep = Annotated[dict, Depends(common_parameters)]

@router.get("/common-items")
async def read_items(commons: CommonDep):
    return commons


@router.get("/common-users")
async def read_users(commons: CommonDep):
    return commons
