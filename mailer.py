import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import csv

# -------------------- CONFIGURATION --------------------
SMTP_SERVER = "smtp.gmail.com"   # Gmail
SMTP_PORT = 465                  # SSL port
SENDER_EMAIL = "ketakidhotre3@gmail.com"
PASSWORD = "dgzw vxkr keak nvpb"   # Use Gmail App Password
RESUME_FILE = "YOUR_RESUME_PDF.pdf"       # Resume file path
CSV_FILE = "emails.csv"          # CSV with only emails
SUBJECT_FILE = "subject.txt"     # File containing subject
BODY_FILE = "body.txt"           # File containing mail body

# -------------------- FUNCTION --------------------
def send_mail(receiver_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = receiver_email
        msg["Subject"] = subject

        # Add body text
        msg.attach(MIMEText(body, "plain"))

        # Attach resume
        with open(RESUME_FILE, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename={RESUME_FILE}",
        )
        msg.attach(part)

        # Send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, context=context) as server:
            server.login(SENDER_EMAIL, PASSWORD)
            server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())

        print(f"✅ Mail sent to {receiver_email}")
    except Exception as e:
        print(f"❌ Could not send mail to {receiver_email}: {e}")

# -------------------- MAIN SCRIPT --------------------
if __name__ == "__main__":
    # Read subject and body once
    with open(SUBJECT_FILE, "r", encoding="utf-8") as sf:
        subject_text = sf.read().strip()
    with open(BODY_FILE, "r", encoding="utf-8") as bf:
        body_text = bf.read()

    # Read email list
    with open(CSV_FILE, newline="", encoding="utf-8") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            receiver_email = row[0].strip()
            if receiver_email:
                send_mail(receiver_email, subject_text, body_text)
