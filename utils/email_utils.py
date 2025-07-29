import smtplib
from email.message import EmailMessage

def send_email_with_attachment(
    *,
    sender_email,
    sender_password,
    receiver_email,
    subject: str,
    body: str,
    attachment_buffer,
    file_name: str,
    smtp_server: str = 'smtp.gmail.com',
    smtp_port: int = 587
):
    if isinstance(receiver_email, str):
        receiver_email = [receiver_email]

    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = ', '.join(receiver_email)
    msg.set_content(body)

    # Add attachment
    attachment_buffer.seek(0)
    msg.add_attachment(attachment_buffer.read(),
                       maintype="application",
                       subtype="pdf",
                       filename=file_name)

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        if not sender_password:
            raise ValueError("Password not provided")
        server.login(sender_email, sender_password)
        server.send_message(msg)

    return True

def send_plain_email(sender_email, sender_password, receiver_email, subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = ", ".join(receiver_email)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)