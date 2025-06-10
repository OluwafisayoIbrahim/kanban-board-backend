from pydantic import BaseModel, EmailStr
from typing import Optional

class UserSignUp(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserSignIn(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict

class User(BaseModel):
    id: str
    username: Optional[str]
    email: EmailStr
    profile_picture_url: Optional[str] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    profile_picture_url: Optional[str] = None
