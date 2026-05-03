import smtplib
from email.message import EmailMessage

def send_email(file_path):
    msg = EmailMessage()
    msg["Subject"] = "Monthly Sales Report"
    msg["From"] = "you@example.com"
    msg["To"] = "receiver@example.com"

    with open(file_path, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename="report.pdf")

    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.starttls()
        s.login("your_email", "your_password")
        s.send_message(msg)