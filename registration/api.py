from pydantic import BaseModel
from fastapi import FastAPI, status
import uvicorn

from db import add as add_to_db
from security import hash_password, verify_password


app = FastAPI()


class User(BaseModel):
    """User data model"""

    name: str
    email: str
    password: str


@app.post('/reg')
def register(user: User):
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
    result: bool = add_to_db(user.name, user.email, hashed_password)

    if result is True:
        return {"result": 1}
    else:
        return {"result": 0}

# Add authentification for User data verifying


if __name__ == '__main__':
    # For testing only
    uvicorn.run(app, host='localhost', port=8002)
