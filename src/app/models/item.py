from pydantic import BaseModel, Field, HttpUrl


class Tag(BaseModel):
    name: str
    version: str

class Image(BaseModel):
    url: HttpUrl | None = None
    name: str

class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(
        gt=0,
        description="цена должна быть больше нуля",
    )
    tax: float | None = None
    tags: list[Tag] = Field(default_factory=list)
    image: Image | None = None
