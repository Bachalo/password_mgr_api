#

from pydantic import BaseModel

class UserInfo(BaseModel):
    name: str
    email: str
    password: str

class LoginInfo(BaseModel):
    email: str
    password: str

class NewPassInfo(BaseModel):
    password: str
    email: str
    url: str