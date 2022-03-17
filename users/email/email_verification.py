from email import message
from django.conf import settings
from django.core.mail import send_mail

from users import email


class verification:

    with open(f'{settings.BASE_DIR}/users/email/html_verification.html') as file:
        html = file.read()

    def __init__(self, name, recipient, code):
        self.name = name
        self.recipient = recipient
        self.code = code

    def send(self):
        html = self.html
        html = html.replace('[name]', self.name)
        html = html.replace('[code]', self.code)
        return send_mail(subject=f'{self.code} is your email verification', message=f'{self.code} is your email verification', from_email=settings.DEFAULT_FROM_EMAIL, recipient_list=['', self.recipient], html_message=html, fail_silently=False)
