from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import Session, select

from ..db import get_session
from ..deps import get_current_user_optional
from ..models import User
from ..security import create_access_token, hash_password, verify_password
from ..settings import settings
from ._schemas import AuthLoginIn, AuthRegisterIn, UserMeOut

router = APIRouter()


@router.post("/register", response_model=UserMeOut)
def register(body: AuthRegisterIn, session: Session = Depends(get_session)) -> UserMeOut:
    exists = session.exec(select(User).where(User.username == body.username)).first()
    if exists:
        raise HTTPException(400, "Username already exists")

    user = User(
        username=body.username,
        email=body.email,
        password_hash=hash_password(body.password),
        is_admin=False,
        permissions=0,
        must_change_password=False,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return UserMeOut(**user.model_dump())


@router.post("/login", response_model=UserMeOut)
def login(
    body: AuthLoginIn,
    response: Response,
    session: Session = Depends(get_session),
) -> UserMeOut:
    user = session.exec(select(User).where(User.username == body.username)).first()
    if not user or not user.password_hash:
        raise HTTPException(401, "Invalid credentials")
    if not verify_password(body.password, user.password_hash):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token(sub=user.username)
    response.set_cookie(
        key=settings.cookie_name,
        value=token,
        httponly=True,
        samesite="lax",
        secure=settings.cookie_secure,
        max_age=settings.jwt_ttl_minutes * 60,
        path="/",
    )
    return UserMeOut(**user.model_dump())


@router.post("/logout")
def logout(response: Response) -> dict[str, bool]:
    response.delete_cookie(key=settings.cookie_name, path="/")
    return {"ok": True}


@router.get("/me", response_model=UserMeOut)
def me(user=Depends(get_current_user_optional)) -> UserMeOut:
    if not user:
        raise HTTPException(401, "Not logged in")
    return UserMeOut(**user.model_dump())
