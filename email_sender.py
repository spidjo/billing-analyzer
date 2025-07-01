import smtplib
from email.message import EmailMessage
import os

def send_email_with_attachment(
    sender_email: str,
    receiver_email,  # Accept str or list[str]
    subject: str,
    body: str,
    pdf_path: str,
    smtp_server: str = 'smtp.gmail.com',
    smtp_port: int = 587,
    sender_password: str = None
):
    if isinstance(receiver_email, str):
        receiver_email = [receiver_email]

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = ', '.join(receiver_email)
    msg.set_content(body)

    with open(pdf_path, 'rb') as f:
        pdf_data = f.read()
    msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename=os.path.basename(pdf_path))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        if not sender_password:
            raise ValueError("Password not provided")
        server.login(sender_email, sender_password)
        server.send_message(msg)

    return True
