from pydantic import BaseModel
from datetime import datetime


class User(BaseModel):
    username: str
    password: str
    created_at: datetime


class ReqUser(BaseModel):
    username: str
    password: str


class ReqMetadata(BaseModel):
    created_at: datetime


class RequestBody(BaseModel):
    user: User
    metadata: ReqMetadata


class Request(BaseModel):
    body: str
    iv: str
