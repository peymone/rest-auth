from pydantic import BaseModel, Field


class UserReg(BaseModel):
    """User data model for registration"""

    name: str = Field(min_length=2, max_length=20)
    email: str = Field(pattern=r"^\S+@\S+\.\S+$")
    password: str = Field(min_length=5)


class UserGet(BaseModel):
    """User data model for getting data"""

    id: int
    name: str
    email: str


class Token(BaseModel):
    """JWT Token data model"""

    access_token: str
    token_type: str


class HTTPError(BaseModel):
    detail: str
