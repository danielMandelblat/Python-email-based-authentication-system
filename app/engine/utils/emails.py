from django.conf import settings
import socket

hostname = socket.gethostname()
IPAddr = socket.gethostbyname(hostname)


from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def send(email: str, code: str, uuid):
    subject = 'Authentication Code'
    html_message = render_to_string('mail_template.html', {'email': email, 'code': code, 'uuid': uuid, 'ip': IPAddr})
    plain_message = strip_tags(html_message)
    from_email = settings.FROM_EMAIL
    to = email

    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)
