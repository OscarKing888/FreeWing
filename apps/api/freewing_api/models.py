from __future__ import annotations

from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel

PERM_UPLOAD = 1
PERM_MODIFY = 2
PERM_DELETE = 4
PERM_DOWNLOAD = 8


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: Optional[str] = Field(default=None, index=True, unique=True)

    password_hash: Optional[str] = Field(default=None)
    is_admin: bool = Field(default=False)
    permissions: int = Field(default=0)

    must_change_password: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class Photo(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    file_path: str = Field(index=True, unique=True)
    file_kind: str = Field(default="image")
    original_mime: Optional[str] = None

    taken_at: Optional[datetime] = Field(default=None, index=True)
    place_text: Optional[str] = Field(default=None, index=True)

    gps_lat: Optional[float] = None
    gps_lng: Optional[float] = None
    geohash: Optional[str] = Field(default=None, index=True)

    species_name: Optional[str] = Field(default=None, index=True)
    starred_count: int = Field(default=0)

    status: str = Field(default="indexed", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class PhotoUserFlag(SQLModel, table=True):
    user_id: int = Field(primary_key=True, foreign_key="user.id")
    photo_id: int = Field(primary_key=True, foreign_key="photo.id")
    starred: bool = Field(default=False, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
