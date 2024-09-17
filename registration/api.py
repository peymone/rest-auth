from pydantic import BaseModel
from fastapi import FastAPI, status
import uvicorn

from db import add_user as add_user_to_db
from db import get_password as get_password_from_db
from security import hash_password, verify_password


app = FastAPI()


class UserReg(BaseModel):
    """User data model for registration"""

    name: str
    email: str
    password: str


class UserAuth(BaseModel):
    """User data model for authentification"""

    email: str
    password: str


@app.post('/reg')
def register(user: UserReg):
    """Register new User by adding to Data Base

    Args:
        name (str): user name
        email (str): user email
        password (str): user password

    Returns:
        json (int): return 1 if User added successfully or 0 otherwise
    """

    # Hash password and add User data to DB
    hashed_password = hash_password(user.password)
    result: bool = add_user_to_db(user.name, user.email, hashed_password)

    if result is True:
        return {"result": 1}
    else:
        return {"result": 0}


@app.post('/auth')
def authentificate(user: UserAuth):
    user_data = get_password_from_db(user.email)

    if user_data is None:
        return {'result': "user email is invalid or not exist"}
    else:
        if verify_password(user.password, user_data[0]):
            return {'result': 1}
        else:
            return {'result': 0}


if __name__ == '__main__':
    # For testing only
    uvicorn.run(app, host='localhost', port=8002)
