import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")
SMTP_FROM = os.getenv("SMTP_FROM", SMTP_USER)  # fallback to SMTP_USER if not set


def send_email(to: str, subject: str, body: str):
    """
    Send an email using SMTP credentials from environment variables.

    Args:
        to (str): Recipient email address
        subject (str): Email subject
        body (str): Email body (plain text)
    """
    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = SMTP_FROM
        msg["To"] = to

        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASS)
            server.sendmail(SMTP_FROM, [to], msg.as_string())

        print(f"✅ Email sent to {to}")

    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        raise  # re-raise so calling function can handle it
