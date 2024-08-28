from django.conf import settings
from django.core.mail import send_mail
from datetime import datetime

def send(email: str, code: str):
    subject = 'Authentication Code'
    message = f'Hi {email}, your authentication code is: {code}'
    email_from = settings.FROM_EMAIL
    recipient_list = [email, ]
    send_mail(subject, message, email_from, recipient_list )

    print(f"{datetime.now()} | Email was sent ({email}|{code})")