from datetime import datetime, timedelta, timezone
from typing import Annotated


from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


from jose import jwt, JWSError
from pydantic import BaseModel


from .hash_password import verify_password, get_password_hash
from .get_token import create_access_token
from .models import UserInDB, Token, TokenData, User
from .constants import ALGORITHM, SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, fake_users_db

from .service import authenticate_user, get_current_active_user


router = APIRouter(tags=["auth-jwt"])


@router.post("/token-jwt")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/users/mejwt")
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return [{"item_id": "Foo", "owner": current_user.username}]