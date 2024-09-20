from pydantic import BaseModel


class UserReg(BaseModel):
    """User data model for registration"""

    name: str
    email: str
    password: str


class UserAuth(BaseModel):
    """User data model for authentification"""

    name: str
    password: str


class UserGet(BaseModel):
    """User data model for getting data"""

    id: int
    name: str
    email: str


class Token(BaseModel):
    """JWT Token data model"""

    access_token: str
    token_type: str = 'Bearer'


class NoToken(BaseModel):

    access_token: bool = None
