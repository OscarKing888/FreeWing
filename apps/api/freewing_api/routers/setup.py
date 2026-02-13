from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from ..db import get_session
from ..models import User
from ..security import hash_password
from ._schemas import SetupAdminPasswordIn

router = APIRouter()


@router.post("/set-admin-password")
def set_admin_password(
    body: SetupAdminPasswordIn,
    session: Session = Depends(get_session),
) -> dict[str, bool]:
    admin = session.exec(select(User).where(User.username == body.username)).first()
    if not admin:
        admin = User(
            username=body.username,
            is_admin=True,
            permissions=0,
            password_hash=None,
            must_change_password=True,
        )
        session.add(admin)
        session.commit()
        session.refresh(admin)

    if admin.password_hash is not None:
        raise HTTPException(status_code=400, detail="Admin password already set")

    admin.password_hash = hash_password(body.new_password)
    admin.must_change_password = False
    session.add(admin)
    session.commit()
    return {"ok": True}
