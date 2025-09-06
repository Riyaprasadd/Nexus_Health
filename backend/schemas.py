from pydantic import BaseModel, EmailStr
from typing import List, Optional


# ----------------- User Schemas -----------------
class RegisterUser(BaseModel):
    username: str
    email: EmailStr
    age: int
    gender: str
    password: str


class LoginUser(BaseModel):
    email: EmailStr
    password: str


class ResetPassword(BaseModel):
    email: EmailStr
    new_password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    age: int
    gender: str

    class Config:
        orm_mode = True


# ----------------- Chat Schemas -----------------
class ChatRequest(BaseModel):
    user: str
    message: str
    language: Optional[str] = "en"


class ChatResponse(BaseModel):
    response: str

    class Config:
        orm_mode = True


# ----------------- Chat History Schemas -----------------
class ChatHistoryItem(BaseModel):
    sender: str
    message: str

    class Config:
        orm_mode = True


class ChatHistoryResponse(BaseModel):
    username: str
    language: str
    history: List[ChatHistoryItem]

    class Config:
        orm_mode = True
