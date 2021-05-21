from pydantic import BaseModel


class User(BaseModel):
    first_name: str
    last_name: str
    email: str


class Verification(BaseModel):
    id: int
    auth_code: int
