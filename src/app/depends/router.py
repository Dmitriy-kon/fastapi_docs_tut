from typing import Annotated
from fastapi import APIRouter, Depends, Cookie


router = APIRouter(tags=["depends"])

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


class CommonQueryParams:
    def __init__(self, q: str = None, skip: int = 0, limit: int = 100) -> None:
        self.q = q
        self.skip = skip
        self.limit = limit
        

async def common_parameters(q: str = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}

def query_extractor(q: str = None):
    return q

def query_or_cookie_extractor(
    q: Annotated[str, Depends(query_extractor)],
    last_query: Annotated[str, Cookie()] = None,
):
    if not q:
        return last_query
    return q


CommonDep = Annotated[dict, Depends(common_parameters)]


@router.get("/items-query")
async def read_query(
    query_or_default: Annotated[str, Depends(query_or_cookie_extractor)],
):
    return {"q_or_cookie": query_or_default}

@router.get("/common-items")
async def read_items_class(commons: Annotated[CommonQueryParams, Depends(CommonQueryParams)]):
    response = {}
    if commons.q:
        response |= {"q": commons.q}
    items = fake_items_db[commons.skip : commons.skip + commons.limit]
    response |= {"items": items}
    return response


@router.get("/common-users")
async def read_users(commons: CommonDep):
    return commons
