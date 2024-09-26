# Third-Party Libraries
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
import jwt

# BuiltIn Libraries
import os
from datetime import datetime, timedelta, timezone


def configurate_security() -> tuple:
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    ALGHORITHM = "HS256"
    JWT_SECRET = os.getenv('JWT_SECRET')

   # For tests running
    if JWT_SECRET is None:
        JWT_SECRET = 'some_secret_jwt_key'

    crypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    return JWT_SECRET, ALGHORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, crypt_context


JWT_SECRET, ALGHORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, crypt_context = configurate_security()


def hash_password(password: str) -> str:
    """Hash password

    Args:
        password (str): plain password

    Returns:
        str: hashed password
    """

    hashed_password = crypt_context.hash(password)
    return hashed_password


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password

    Args:
        plain_password (str): non hashed password
        hashed_password (str): hashed password

    Returns:
        bool: return True if password is verified
    """

    try:
        result = crypt_context.verify(plain_password, hashed_password)
        return result
    except UnknownHashError:
        return False


def generate_token(user_data: dict) -> str:
    """Generate JWT Token with PyJWT module

    Args:
        user_data (dict[int]): user_id

    Returns:
        str: JWT Token
    """

    payload = user_data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({'exp': expire})
    encoded_jwt = jwt.encode(payload, JWT_SECRET, ALGHORITHM)

    return encoded_jwt


def verify_token(encoded_jwt: str) -> tuple:
    """Verify JWT Token and return user id

    Args:
        encoded_jwt (str): JWT Token

    Returns:
        tuple: user id, details message
    """

    try:

        payload = jwt.decode(encoded_jwt, JWT_SECRET, algorithms=[ALGHORITHM])
        user_id: int = payload.get('sub')

        if user_id is None:
            return (0, "token data is corrupted")

        return (user_id, 'token is verified')

    except InvalidTokenError:
        return (0, "token data is corrupted")

    except ExpiredSignatureError:
        return (0, "token is expired")
