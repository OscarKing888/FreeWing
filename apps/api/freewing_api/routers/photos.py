from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, select

from ..db import get_session
from ..deps import get_current_user_optional
from ..models import Photo, PhotoUserFlag
from ._schemas import PhotoListOut, PhotoOut

router = APIRouter()


def _thumb_url(photo_id: int) -> str:
    return f"/media/thumb/{photo_id}.jpg"


def _preview_url(photo_id: int) -> str:
    return f"/media/preview/{photo_id}.jpg"


@router.get("", response_model=PhotoListOut)
def list_photos(
    session: Session = Depends(get_session),
    user=Depends(get_current_user_optional),
    cursor: Optional[int] = Query(default=None),
    limit: int = Query(default=40, ge=1, le=100),
    species: Optional[str] = None,
    place: Optional[str] = None,
    only_starred: bool = False,
) -> PhotoListOut:
    stmt = (
        select(Photo)
        .where(Photo.status == "indexed")
        .order_by(Photo.taken_at.desc().nullslast(), Photo.id.desc())
    )
    if cursor is not None:
        stmt = stmt.where(Photo.id < cursor)
    if species:
        stmt = stmt.where(Photo.species_name == species)
    if place:
        stmt = stmt.where(Photo.place_text == place)

    photos: List[Photo] = session.exec(stmt.limit(limit + 1)).all()

    if only_starred:
        if not user:
            return PhotoListOut(items=[], next_cursor=None)
        ids = [p.id for p in photos if p.id is not None]
        if ids:
            flags = session.exec(
                select(PhotoUserFlag).where(
                    PhotoUserFlag.user_id == user.id,
                    PhotoUserFlag.photo_id.in_(ids),
                    PhotoUserFlag.starred.is_(True),
                )
            ).all()
            starred_set = {f.photo_id for f in flags}
            photos = [p for p in photos if p.id in starred_set]

    next_cursor = None
    if len(photos) > limit:
        next_cursor = photos[limit - 1].id
        photos = photos[:limit]

    starred_map = {}
    if user:
        ids = [p.id for p in photos if p.id is not None]
        if ids:
            flags = session.exec(
                select(PhotoUserFlag).where(
                    PhotoUserFlag.user_id == user.id,
                    PhotoUserFlag.photo_id.in_(ids),
                )
            ).all()
            starred_map = {f.photo_id: f.starred for f in flags}

    items = [
        PhotoOut(
            id=p.id,
            taken_at=p.taken_at,
            place_text=p.place_text,
            species_name=p.species_name,
            thumb_url=_thumb_url(p.id),
            preview_url=_preview_url(p.id),
            is_starred=starred_map.get(p.id) if user else None,
        )
        for p in photos
        if p.id is not None
    ]
    return PhotoListOut(items=items, next_cursor=next_cursor)
