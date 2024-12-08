import imaplib
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email import message_from_bytes

from dotenv import dotenv_values

config = dotenv_values(".env")

EMAIL = config["EMAIL"]
PASSWORD = config["PASSWORD"]
IMAP_SERVER = config["IMAP_SERVER"]
SMTP_SERVER = config["SMTP_SERVER"]
SMTP_PORT = int(config["SMTP_PORT"])


def get_emails():
    try:
        print("Łączenie z serwerem IMAP...")
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        print("Zalogowano do skrzynki pocztowej.")

        mail.select("INBOX")
        status, messages = mail.search(None, 'ALL')  # Zmień na 'UNSEEN' po testach
        if status == "OK" and messages[0]:
            for num in messages[0].split():
                status, data = mail.fetch(num, '(RFC822)')
                if status == "OK":
                    msg = message_from_bytes(data[0][1])
                    sender = msg['From']
                    subject = msg['Subject']
                    body = extract_email_body(msg)
                    d = dict(msg=msg, sender=sender, subject=subject, body=body)
                    yield d
        else:
            print("Brak nowych wiadomości.")
        mail.logout()
    except Exception as e:
        print(f"Błąd podczas sprawdzania wiadomości: {e}")


def extract_email_body(msg):
    body = None
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))
            if content_type == "text/plain" and "attachment" not in content_disposition:
                body = part.get_payload(decode=True)
                if body:
                    return body.decode('utf-8', errors='ignore')
    else:
        body = msg.get_payload(decode=True)
        if body:
            return body.decode('utf-8', errors='ignore')
    return "Brak treści w wiadomości."


def send_email(to_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL, PASSWORD)
            server.send_message(msg)
        print(f"Wysłano odpowiedź do {to_email}")
    except Exception as e:
        print(f"Błąd podczas wysyłania wiadomości do {to_email}: {e}")


if __name__ == "__main__":
    emails = get_emails()
    for email in emails:
        print('email:', email)
