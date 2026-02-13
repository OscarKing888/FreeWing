from fastapi import Depends, HTTPException, Request, status
from sqlmodel import Session, select

from .db import get_session
from .models import User
from .security import decode_token
from .settings import settings


def get_current_user_optional(
    request: Request,
    session: Session = Depends(get_session),
) -> User | None:
    token = request.cookies.get(settings.cookie_name)
    if not token:
        return None
    try:
        payload = decode_token(token)
        username = payload.get("sub")
        if not username:
            return None
        return session.exec(select(User).where(User.username == username)).first()
    except Exception:
        return None


def require_user(user: User | None = Depends(get_current_user_optional)) -> User:
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not logged in",
        )
    return user


def require_permission(bit: int):
    def _dep(user: User = Depends(require_user)) -> User:
        if user.is_admin:
            return user
        if (user.permissions & bit) != bit:
            raise HTTPException(status_code=403, detail="Permission denied")
        return user

    return _dep
