from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class AuthRegisterIn(BaseModel):
    username: str = Field(min_length=3, max_length=32)
    email: Optional[str] = None
    password: str = Field(min_length=8, max_length=128)


class AuthLoginIn(BaseModel):
    username: str
    password: str


class UserMeOut(BaseModel):
    id: int
    username: str
    email: Optional[str]
    is_admin: bool
    permissions: int
    must_change_password: bool


class ChangePasswordIn(BaseModel):
    old_password: Optional[str] = None
    new_password: str = Field(min_length=8, max_length=128)


class SetupAdminPasswordIn(BaseModel):
    username: str = "admin"
    new_password: str = Field(min_length=8, max_length=128)


class PhotoOut(BaseModel):
    id: int
    taken_at: Optional[datetime]
    place_text: Optional[str]
    species_name: Optional[str]
    thumb_url: str
    preview_url: str
    is_starred: Optional[bool] = None


class PhotoListOut(BaseModel):
    items: List[PhotoOut]
    next_cursor: Optional[int] = None
