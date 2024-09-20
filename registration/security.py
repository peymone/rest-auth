from passlib.context import CryptContext
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from datetime import datetime, timedelta, timezone


# Remove it from here
SECRET_KEY = "some_really_secret_key"
ALGHORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

crypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


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

    result = crypt_context.verify(plain_password, hashed_password)
    return result


def generate_token(user_data: dict) -> str:
    payload = user_data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload.update({'exp': expire})
    encoded_jwt = jwt.encode(payload, SECRET_KEY, ALGHORITHM)

    return encoded_jwt


def verify_token(encoded_jwt: str) -> int:

    try:

        payload = jwt.decode(encoded_jwt, SECRET_KEY, algorithms=[ALGHORITHM])
        user_id: int = payload.get('sub')

        if user_id is None:
            return 0

        return user_id

    except InvalidTokenError:
        print("Token data is carrupted")
        return 0

    except ExpiredSignatureError:
        print("Token is expired")
        return 0
