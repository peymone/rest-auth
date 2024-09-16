from passlib.context import CryptContext


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
