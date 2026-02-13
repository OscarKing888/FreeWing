from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from ..db import get_session
from ..deps import require_user
from ..security import hash_password, verify_password
from ._schemas import ChangePasswordIn, UserMeOut

router = APIRouter()


@router.post("/me/change-password", response_model=UserMeOut)
def change_password(
    body: ChangePasswordIn,
    session: Session = Depends(get_session),
    user=Depends(require_user),
) -> UserMeOut:
    if user.password_hash and body.old_password:
        if not verify_password(body.old_password, user.password_hash):
            raise HTTPException(400, "Old password incorrect")

    user.password_hash = hash_password(body.new_password)
    user.must_change_password = False
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserMeOut(**user.model_dump())
