import threading
import time

from dotenv import dotenv_values

from email_checker import get_emails, send_email
from gpt_bot import generate_response

config = dotenv_values(".env")


def main():
    while True:
        emails = get_emails()
        for email in emails:
            thread = threading.Thread(target=handle_message, args=(email["sender"], email["subject"], email["body"]))
            thread.start()
        time.sleep(60)


def handle_message(sender, subject, body):
    try:
        print(f"Generowanie odpowiedzi dla: {sender}")
        response = generate_response(body)
        send_email(sender, f"Odpowiedź: {subject}", response)
    except Exception as e:
        print(f"Błąd podczas obsługi wiadomości od {sender}: {e}")


if __name__ == "__main__":
    email_thread = threading.Thread(target=main)
    email_thread.daemon = True
    email_thread.start()
    while True:
        time.sleep(1)
