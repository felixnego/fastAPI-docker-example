from pydantic import BaseModel, Field, EmailStr


# pydantic uses the Ellipsis object
# to indicate required fields

class UserModel(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)


class UserLoginModel(BaseModel):
    email: EmailStr = Field(...)
    password: str = Field(...)