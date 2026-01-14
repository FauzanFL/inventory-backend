from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from .config import settings

import bcrypt


def create_access_token(subject: Union[str, Any], role: str) -> str:
    expire = datetime.now(datetime.timezone.utc) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode = {"exp": expire, "sub": str(subject), "role": role}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        plain_password.encode("utf-8"),
        hashed_password.encode("utf-8"),
    )

def get_password_hash(password: str) -> str:
    pwd_bytes = password.encode("utf-8")

    salt = bcrypt.gensalt()
    hashed_pass = bcrypt.hashpw(pwd_bytes, salt)
    return hashed_pass.decode("utf-8")