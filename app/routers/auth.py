from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPAuthorizationCredentials
from datetime import timedelta
from typing import Optional
import re

from app.schemas.user import UserSignUp, UserSignIn, Token, User
from app.db.crud import get_user_by_email, get_user_by_username, create_user
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.security import verify_password, create_access_token
from app.utils.exceptions import UserAlreadyExists, CredentialsInvalid

router = APIRouter()

def extract_token_from_header(request: Request) -> Optional[str]:
    """Extract Bearer token from Authorization header"""
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return None
    
    if not auth_header.startswith("Bearer "):
        return None
    
    # Extract the token part
    token = auth_header[7:]  
    return token if token else None

def decode_jwt_token(token: str) -> Optional[str]:
    """Decode JWT token and return email"""
    try:
        from jose import JWTError, jwt
        from app.core.config import SECRET_KEY, ALGORITHM
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        return email
    except JWTError:
        return None

@router.post("/signup", response_model=Token)
async def sign_up(data: UserSignUp):
    if get_user_by_email(data.email):
        raise UserAlreadyExists("email")
    if get_user_by_username(data.username):
        raise UserAlreadyExists("username")
    
    user_id = create_user(data.username, data.email, data.password)
    if not user_id:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create user",
        )
    
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(subject=data.email, expires_delta=expires)
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user={"id": user_id, "username": data.username, "email": data.email},
    )

@router.post("/signin", response_model=Token)
async def sign_in(data: UserSignIn):
    user = get_user_by_email(data.email)
    if not user or not verify_password(data.password, user[3]):
        raise CredentialsInvalid()
    
    expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(subject=data.email, expires_delta=expires)
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        user={"id": user[0], "username": user[1], "email": user[2]},
    )
    
@router.get("/me")
async def get_current_user_simple(request: Request):
    """Get current user info - Method 4 (Simplest)"""
    auth_header = request.headers.get("Authorization", "")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        return {"error": "No valid authorization header", "status": 401}
    
    token = auth_header.split(" ")[1]
    
    try:
        from jose import jwt
        from app.core.config import SECRET_KEY, ALGORITHM
        
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        
        if email:
            user = get_user_by_email(email)
            if user:
                return {
                    "id": user[0],
                    "username": user[1], 
                    "email": user[2],
                    "status": "success"
                }
    except:
        pass
    
    return {"error": "Authentication failed", "status": 401}