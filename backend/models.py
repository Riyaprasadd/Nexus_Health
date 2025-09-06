from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from backend.database import Base


# ----------------- User Model -----------------
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(10), nullable=False)  # male / female / other
    password = Column(String(255), nullable=False)
    language = Column(String(10), default="en")  # default English

    # Relationship → One user can have many chats
    chats = relationship("ChatHistory", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"


# ----------------- Chat History -----------------
class ChatHistory(Base):
    __tablename__ = "chat_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    sender = Column(String(10), nullable=False)  # "user" or "bot"
    message = Column(Text, nullable=False)

    # Relationship → Links back to User
    user = relationship("User", back_populates="chats")

    def __repr__(self):
        return f"<ChatHistory(id={self.id}, user_id={self.user_id}, sender='{self.sender}')>"


# ----------------- Medical QnA -----------------
class MedicalQnA(Base):
    __tablename__ = "medical_qna"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, unique=True, nullable=False)
    answer = Column(Text, nullable=False)

    def __repr__(self):
        return f"<MedicalQnA(id={self.id}, question='{self.question[:30]}...')>"
