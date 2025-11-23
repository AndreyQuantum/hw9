from pydantic import BaseModel, EmailStr


class CreateUser(BaseModel):
    full_name: str
    email: EmailStr
    password: str

class GetUser(BaseModel):
    id: int
    email: EmailStr
    full_name: str
