from pydantic import BaseModel


class Verification(BaseModel):
    first_name: str
    last_name: str
    email: str
    school: str
