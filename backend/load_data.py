import os
import pandas as pd
from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine, Base
from backend.models import MedicalQnA

# ----------------- File Path -----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, "data", "medical_qna.csv")

if not os.path.exists(csv_path):
    raise FileNotFoundError(f"❌ CSV file not found at {csv_path}")

# ----------------- Reset medical_qna Table -----------------
print("🔄 Resetting medical_qna table...")
Base.metadata.drop_all(bind=engine, tables=[MedicalQnA.__table__])
Base.metadata.create_all(bind=engine, tables=[MedicalQnA.__table__])

# ----------------- Load CSV -----------------
df = pd.read_csv(csv_path)

print("📌 Available columns in CSV:", df.columns.tolist())

# ✅ Normalize column names
if "input" in df.columns and "output" in df.columns:
    df = df.rename(columns={"input": "question", "output": "answer"})
elif not {"question", "answer"}.issubset(df.columns):
    raise ValueError("❌ CSV must contain either 'input/output' or 'question/answer' columns")

# ----------------- Insert into DB -----------------
db: Session = SessionLocal()
inserted = 0

try:
    for _, row in df.iterrows():
        if pd.isna(row["question"]) or pd.isna(row["answer"]):
            continue  # skip empty rows
        qna = MedicalQnA(
            question=str(row["question"]).strip(),
            answer=str(row["answer"]).strip()
        )
        db.add(qna)
        inserted += 1

    db.commit()
    print(f"✅ {inserted} QnA records inserted into database successfully!")

except Exception as e:
    db.rollback()
    print(f"❌ Error inserting data: {e}")

finally:
    db.close()
