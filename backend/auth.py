import os
from passlib.hash import bcrypt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from datetime import datetime

from .database import add_user, get_user


SECRET_KEY = os.getenv("SECRET_KEY", "change_me")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


security = HTTPBearer()


# ---- Passwords ----


def hash_password(password: str) -> str:
    return bcrypt.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.verify(password, password_hash)


# ---- JWT ----


def create_access_token(subject: str, expires_delta:Optional[timedelta] = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"sub": subject, "exp": datetime.utcnow() + expires_delta}
        return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)




def get_current_username(creds: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = creds.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
            return username
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")


# ---- Register/Login ----


def register_user(username: str, password: str):
    if get_user(username):
        raise HTTPException(status_code=400, detail="Username already exists")
        ok = add_user(username, hash_password(password))
        if not ok:
            raise HTTPException(status_code=400, detail="Could not create user")
    return {"message": "Registration successful"}




def login_user(username: str, password: str) -> str:
    row = get_user(username)
    if not row:
        raise HTTPException(status_code=401, detail="Invalid credentials")
        _, _, password_hash, _ = row
        if not verify_password(password, password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
            return create_access_token(subject=username)