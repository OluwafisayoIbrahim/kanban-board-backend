from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
import datetime as dt
from .config import SECRET_KEY, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain,hashed):
    return pwd_context.verify(plain,hashed)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(subject:str, expires_delta: timedelta):
    now = datetime.now(dt.timezone.utc)
    to_encode = {"sub": subject, "iat": now, "exp": now + expires_delta}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)