from pydantic import BaseModel, Field
from typing import List, Optional


class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class ChatRequest(BaseModel):
    message: str
    lang: str = "en"


class Citation(BaseModel):
    label: str
    url: str


class ChatResponse(BaseModel):
    response: str
    intent: str
    citations: List[Citation] = []
    safety_note: Optional[str] = None


class TipResponse(BaseModel):
    tip: str
    category: str