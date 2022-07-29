from typing import List, Union

from pydantic import BaseModel


class BaseMasterPassword(BaseModel):
    hint: str


class MasterPasswordCreate(BaseMasterPassword):
    master_password: str


class MasterPassword(BaseMasterPassword):
    class Config:
        orm_mode = True


class BasePassword(BaseModel):
    name: str
    url: str


class PasswordCreate(BasePassword):
    user_name: str
    password: str


class Password(BasePassword):
    id: int

    class Config:
        orm_mode = True


class AllPassword(BasePassword):
    id: int
    user_name: str
    password: str

    class Config:
        orm_mode = True
