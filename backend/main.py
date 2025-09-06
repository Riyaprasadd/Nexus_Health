from difflib import get_close_matches
import os
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from contextlib import asynccontextmanager
from datetime import datetime, timedelta
import secrets

from fastapi import FastAPI, Depends, HTTPException, Query, Form, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt, JWTError

from backend.database import init_db, get_db
from backend.models import User, ChatHistory, MedicalQnA
from backend.schemas import (
    RegisterUser, LoginUser, ChatRequest, ChatResponse, ChatHistoryResponse
)
from dotenv import load_dotenv

# ----------------- Load Environment -----------------
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))

print("ENV SMTP_USER:", os.getenv("SMTP_USER"))
print("ENV SMTP_PASS:", os.getenv("SMTP_PASS"))

# ----------------- Security -----------------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ----------------- JWT Config -----------------
SECRET_KEY = "supersecretkey123"   # ⚠️ use env variable in production
ALGORITHM = "HS256"
RESET_TOKEN_EXPIRE_MINUTES = 30

# ----------------- Translation -----------------
try:
    from deep_translator import GoogleTranslator
except Exception:
    GoogleTranslator = None


def translate_to_english(msg: str) -> str:
    if GoogleTranslator is None:
        return msg
    try:
        return GoogleTranslator(source="auto", target="en").translate(msg)
    except Exception:
        return msg


def translate_from_english(msg: str, lang_code: str) -> str:
    if not lang_code or lang_code.lower() == "en" or GoogleTranslator is None:
        return msg
    try:
        return GoogleTranslator(source="en", target=lang_code.lower()).translate(msg)
    except Exception:
        return msg


# ----------------- CSV Loader -----------------
def load_csv_to_db(db: Session):
    from sqlalchemy.exc import IntegrityError

    csv_path = os.path.join("backend", "data", "medical_qna.csv")
    if not os.path.exists(csv_path):
        print(f"❌ CSV not found at: {csv_path}")
        return

    df = pd.read_csv(csv_path)

    inserted_count = 0
    skipped_count = 0

    for _, row in df.iterrows():
        question = str(row["input"]).strip()
        answer = str(row["output"]).strip()

        try:
            db.add(MedicalQnA(question=question, answer=answer))
            db.commit()
            inserted_count += 1
        except IntegrityError:
            db.rollback()
            skipped_count += 1

    print(f"✅ CSV load finished. Inserted {inserted_count}, Skipped {skipped_count} (duplicates).")


# ----------------- Lifespan -----------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    db = next(get_db())
    try:
        load_csv_to_db(db)
    finally:
        db.close()
    yield


# ----------------- App -----------------
app = FastAPI(title="Global Wellness Chatbot API", lifespan=lifespan)

# ✅ CORS Middleware
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------- Email Helper -----------------
def send_email(to_email: str, subject: str, body: str):
    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER")
    smtp_pass = os.getenv("SMTP_PASS")
    smtp_from = os.getenv("SMTP_FROM", smtp_user)

    msg = MIMEText(body, "plain", "utf-8")
    msg["Subject"] = subject
    msg["From"] = smtp_from
    msg["To"] = to_email

    try:
        print(f"📨 Connecting to {smtp_host}:{smtp_port} as {smtp_user}")
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_from, [to_email], msg.as_string())
        print("✅ Email sent to:", to_email)
    except Exception as e:
        print("❌ Email send failed:", e)


# ----------------- JWT Helpers -----------------
def create_reset_token(email: str):
    expire = datetime.utcnow() + timedelta(minutes=RESET_TOKEN_EXPIRE_MINUTES)
    data = {"sub": email, "exp": expire}
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def verify_reset_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except JWTError:
        return None


# ----------------- Routes -----------------
@app.get("/")
def root():
    return {"message": "🌍 Global Wellness Chatbot API is running 🚀"}


# ---- Register ----
@app.post("/register")
def register(user: RegisterUser, db: Session = Depends(get_db)):
    email_clean = user.email.strip().lower()
    if db.query(User).filter(User.username == user.username).first():
        raise HTTPException(status_code=400, detail="❌ Username already taken")
    if db.query(User).filter(User.email == email_clean).first():
        raise HTTPException(status_code=400, detail="❌ Email already registered")

    hashed_pw = pwd_context.hash(user.password)
    new_user = User(
        username=user.username.strip(),
        email=email_clean,
        age=int(user.age),
        gender=user.gender.strip().lower(),
        password=hashed_pw,
        language="en",
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "id": new_user.id,
        "username": new_user.username,
        "email": new_user.email,
        "gender": new_user.gender,
        "message": "✅ User registered successfully!"
    }


# ---- Login ----
@app.post("/login")
def login(payload: LoginUser, db: Session = Depends(get_db)):
    email_clean = payload.email.strip().lower()
    user = db.query(User).filter(User.email == email_clean).first()
    if not user or not pwd_context.verify(payload.password, user.password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return {
        "user_id": user.id,
        "username": user.username,
        "language": user.language,
        "message": "Login successful ✅"
    }


# ---- Password Reset Step 1 ----
@app.post("/request-password-reset")
def request_password_reset(
    email: str = Form(...),
    background_tasks: BackgroundTasks = None,
    db: Session = Depends(get_db)
):
    clean_email = email.strip().lower()
    user = db.query(User).filter(User.email == clean_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_reset_token(user.email)
    reset_link = f"http://localhost:3000/reset-password/confirm?token={token}"

    body = f"""
    Hi {user.username},

    Click the link below to reset your password:
    {reset_link}

    ⚠️ This link expires in 30 minutes.
    """

    if background_tasks:
        background_tasks.add_task(send_email, user.email, "Password Reset Request", body)
    else:
        send_email(user.email, "Password Reset Request", body)

    return {"message": "Password reset link sent to email"}


# ---- Password Reset Step 2 ----
@app.post("/reset-password/confirm")
def reset_password_confirm(
    token: str = Form(...),
    new_password: str = Form(...),
    db: Session = Depends(get_db)
):
    email = verify_reset_token(token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_pw = pwd_context.hash(new_password)
    user.password = hashed_pw
    db.commit()

    return {"message": "✅ Password has been reset successfully"}


# ---- Chat ----
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == request.user).first()

    if not user:  # guest fallback
        class Guest:
            id = 0
            username = request.user or "guest"
            language = request.language or "en"
        user = Guest()

    if user.id != 0:
        db.add(ChatHistory(user_id=user.id, sender="user", message=request.message))

    query_en = translate_to_english(request.message).lower()
    all_qna = db.query(MedicalQnA).all()

    if all_qna:
        all_questions = [q.question for q in all_qna]
        matches = get_close_matches(query_en, [q.lower() for q in all_questions], n=1, cutoff=0.5)
        if matches:
            matched_qna = next(q for q in all_qna if q.question.lower() == matches[0])
            bot_reply = matched_qna.answer
        else:
            bot_reply = "Sorry, I don’t have information about that. Please rephrase your question."
    else:
        bot_reply = "Knowledge base is empty. Please add QnA data."

    lang_map = {"english": "en", "hindi": "hi"}
    out_lang = lang_map.get(request.language.strip().lower(), "en") if request.language else (user.language or "en")
    bot_reply_translated = translate_from_english(bot_reply, out_lang)

    if user.id != 0:
        db.add(ChatHistory(user_id=user.id, sender="bot", message=bot_reply_translated))
        db.commit()

    return {"response": bot_reply_translated}


# ---- History ----
@app.get("/history/{username}", response_model=ChatHistoryResponse)
def get_history(username: str, limit: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    rows = (
        db.query(ChatHistory)
        .filter(ChatHistory.user_id == user.id)
        .order_by(ChatHistory.id.desc())
        .limit(limit)
        .all()
    )
    rows = list(reversed(rows))

    return {
        "username": user.username,
        "language": user.language,
        "history": [{"sender": r.sender, "message": r.message} for r in rows],
    }


print("SMTP_USER:", os.getenv("SMTP_USER"))
print("SMTP_PASS:", os.getenv("SMTP_PASS"))
