from pydantic import BaseModel, Field


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
