# Third-Party Libraries
from fastapi import FastAPI

# My Modules
from .models import *
from .db import init_db
from .db import add_user as add_user_to_db
from .db import get_user_by_name, get_user_by_id
from .security import hash_password, verify_password, generate_token, verify_token

# Configurate app
app = FastAPI()
init_db()


@app.post('/verify_token')
def token_check(token: dict) -> dict:

    result = verify_token(token['access_token'])
    return {'user_id': result[0]}


@app.post('/reg')
def register(user: UserReg) -> dict:
    """Register new User by adding to Data Base

    Args:
        name (str): user name
        email (str): user email
        password (str): user password

    Returns:
        dict (int | None): return user_id if User added successfully or None otherwise
    """

    # Hash password and add User data to DB
    hashed_password = hash_password(user.password)
    user_id: int | None = add_user_to_db(user.name, user.email, hashed_password)

    # Return user id
    if user_id is None:
        return {'user_id': None}
    else:
        return {'user_id': user_id}


@app.post('/auth')
def authentificate(user: UserAuth) -> Token | NoToken:
    """Authentificate user and return JWT token

    Args:
        user (UserAuth): user.name (str), user.password (str)

    Returns:
        Token | NoToken: Token.access_token (str), Token.token_type (str) OR Token.access_token (None)
    """

    user_data = get_user_by_name(user.name)

    if user_data is None:
        return NoToken

    user_id, user_email, user_password = user_data

    if verify_password(user.password, user_password) is True:
        jwt_token = generate_token({'sub': user_id})
        return Token(access_token=jwt_token)
    else:
        return NoToken


@app.get('/user')
def get_current_user(user_id: int) -> UserGet:
    """Get logged in user data by his id"""

    user_data = get_user_by_id(user_id)

    if user_data is None:
        return UserGet

    user_name, user_email, user_password = user_data
    return UserGet(id=user_id, name=user_name, email=user_email)
