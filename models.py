#
from typing import List
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
    url_address: str

class EditPassInfo(BaseModel):
    url_address: str
    email: str
    password: str
    valueToChange: str
    newValue: str

class SearchPassInfo(BaseModel):
    searchTerm: str


class SearchResult(BaseModel):
    id: int
    password: str
    email: str
    url_address: str
    username: str

def process_searchResult_list(items: List[SearchResult]):
    pass