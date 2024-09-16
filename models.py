from pydantic import BaseModel, Field


class User(BaseModel):
    """User data model"""

    name: str = Field(min_lenght=2, max_length=20)
    email: str
    password: str = Field(min_length=5)
