from pydantic import BaseModel, EmailStr

class Usercreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    username: str
    password: str