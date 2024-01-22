from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    full_name: str | None = None

class UserIn(User):
    password: str