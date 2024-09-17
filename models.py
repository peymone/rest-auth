from pydantic import BaseModel, Field


class UserReg(BaseModel):
    """User data model for registration"""

    name: str = Field(min_lenght=2, max_length=20)
    email: str
    password: str = Field(min_length=5)


class UserAuth(BaseModel):
    """User data model for authentification"""

    email: str
    password: str
