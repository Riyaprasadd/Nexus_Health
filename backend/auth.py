import os
from datetime import datetime, timedelta
from typing import Optional

from jose import jwt, JWTError, ExpiredSignatureError
from dotenv import load_dotenv

# ----------------- Load environment variables -----------------
load_dotenv()

SECRET_KEY: str = os.getenv("SECRET_KEY", "change_this_secret_key")
ALGORITHM: str = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))


# ----------------- Create JWT Token -----------------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Generate a JWT access token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


# ----------------- Decode JWT Token -----------------
def decode_token(token: str) -> Optional[dict]:
    """
    Decode a JWT token and return the payload.
    Returns None if the token is invalid or expired.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except ExpiredSignatureError:
        print("❌ Token expired")
        return None
    except JWTError:
        print("❌ Invalid token")
        return None
