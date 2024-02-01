from typing import Annotated

from fastapi import Depends, HTTPException, status

from jose import jwt, JWSError

from .constants import ALGORITHM, SECRET_KEY, fake_users_db, oauth2_scheme
from .models import TokenData, User, UserInDB
from .hash_password import verify_password, get_password_hash



def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        print("Incorrect password")
        return False
    return user



async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWSError:
        raise credentials_exception
    
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    create_user: Annotated[User, Depends(get_current_user)]
):
    if create_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return create_user