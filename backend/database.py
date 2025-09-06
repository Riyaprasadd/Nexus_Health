from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# ✅ Path to your SQLite DB
DATABASE_URL = r"sqlite:///C:\Users\riyap\Desktop\chatbot\Global-wellness-chatbot-An-AI-powered-chatbot-that-provides-health-information-\backend\chatbot.db"

# ----------------- Engine -----------------
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

# ----------------- Session -----------------
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# ----------------- Base -----------------
Base = declarative_base()

# ----------------- Init DB -----------------
def init_db():
    import backend.models  # ensure models are imported
    Base.metadata.create_all(bind=engine)

# ----------------- Dependency for FastAPI -----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
