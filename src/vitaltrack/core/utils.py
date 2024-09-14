"""
Authentication utility functions.
"""

from __future__ import annotations

import bcrypt
import datetime
import jwt

from vitaltrack import config


def generate_salt() -> bytes:
    return bcrypt.gensalt()


def get_password_hash(password: bytes, salt: bytes) -> bytes:
    return bcrypt.hashpw(password, salt)


def verify_password(password_to_check: bytes, password_hash: bytes) -> bytes:
    return bcrypt.checkpw(password_to_check, password_hash)


def create_access_token(
    data: dict, expires_delta: datetime.timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.now(datetime.timezone.utc) + expires_delta
    else:
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
            minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
