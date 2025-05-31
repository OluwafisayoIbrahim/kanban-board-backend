from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import timedelta
from app.dependencies import verify_api_key
from app.schemas.user import UserSignUp, UserSignIn, Token, User
from app.db.crud import get_user_by_email, get_user_by_username, create_user
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.security import verify_password, create_access_token
from app.utils.exceptions import UserAlreadyExists, CredentialsInvalid

router = APIRouter()
bearer = HTTPBearer()


async def get_current_user(
    creds: HTTPAuthorizationCredentials = Depends(bearer)
):
    token = creds.credentials
    from jose import JWTError, jwt
    from app.core.config import SECRET_KEY, ALGORITHM

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise JWTError()
    except JWTError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = get_user_by_email(email)
    if user is None:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


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


@router.get("/me", response_model=User)
async def read_me(current_user=Depends(get_current_user)):
    return User(
        id=current_user[0],
        username=current_user[1],
        email=current_user[2]
    )
