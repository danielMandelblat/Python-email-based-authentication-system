from django.db import models
import random, string
from .utils.emails import send
from django.conf import settings
from datetime import timedelta
from django.db.models.functions import Now
from os import getenv

def generate_password(length: int=8)-> str:
    # add lower case chars
    lower  = [random.choice(string.ascii_lowercase) for i in range(length)]
    # add digit chars
    digit  = [random.choice(string.digits) for i in range(length)]
    # add upper case chars
    upper  = [random.choice(string.ascii_uppercase) for i in range(length)]
    # add symbols
    symbol = [random.choice(["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "-", "+", "=", ".", ",", "?"]) for i in range(length)]
    # store random generated lists to a variable
    original = lower+digit+upper+symbol
    # shuffle stored data in place
    random.shuffle(original)
    return ''.join(original)

class SiteSettings(models.Model):
    EMAIL_HOST = models.CharField(max_length=55, default='smtp3.danielmandelblat.com', null=True, blank=True)
    EMAIL_PORT = models.PositiveIntegerField(default=25, null=True, blank=True)
    EMAIL_USE_TLS = models.BooleanField(default=False, null=False, blank=False)
    EMAIL_HOST_USER = models.CharField(max_length=55, null=True, blank=True)
    EMAIL_HOST_PASSWORD = models.CharField(max_length=55, null=True, blank=True)
    FROM_EMAIL = models.CharField(max_length=55, default='auth-system@danielmandelblat.com', null=True, blank=True)
    CODE_TIMEOUT = models.PositiveIntegerField(help_text='How long the latest code is valid in minutes', default=30, null=False, blank=False)

    @classmethod
    def get(cls):
        if cls.objects.all().count() <= 0:
            cls.objects.create()

        settings = cls.objects.all().first()
        settings.refresh_from_db()
        return settings

    def save(self, *args, **kwargs):
        super(SiteSettings, self).save(*args, **kwargs)
        self.apply_settings()

    @classmethod
    def apply_settings(cls):
        # Change settings
        try:
            SS = SiteSettings.get()
            settings.EMAIL_HOST = getenv('EMAIL_HOST', SS.EMAIL_HOST)
            settings.EMAIL_PORT = getenv('EMAIL_PORT', SS.EMAIL_PORT)
            settings.EMAIL_USE_TLS = getenv('EMAIL_USE_TLS', SS.EMAIL_USE_TLS)
            settings.EMAIL_HOST_USER = getenv('EMAIL_HOST_USER', SS.EMAIL_HOST_USER)
            settings.EMAIL_HOST_PASSWORD = getenv('EMAIL_HOST_PASSWORD', SS.EMAIL_HOST_PASSWORD)
            settings.FROM_EMAIL = getenv('FROM_EMAIL', SS.FROM_EMAIL)
            settings.CODE_TIMEOUT = getenv('CODE_TIMEOUT', SS.CODE_TIMEOUT)
            print("New settings has been applied!")
        except Exception as e:
            print(f"Error loading system settings, {e}")


class Log(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    message = models.TextField(null=False, blank=False)
    ip_address = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return f"{self.created_date} | {self.message}"

# Create your models here.
class Email(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(null=False, blank=False)

    @classmethod
    def get_active(self, email: str):
        results = Authentication.objects.filter(email__email=email, active=True, created_date__gte=Now()-timedelta(minutes=SiteSettings.get().CODE_TIMEOUT))
        return results

    @classmethod
    def auth(cls, email: str, code: str):
        result = cls.get_active(email=email)

        if result.count() == 0:
            raise Exception(f"There is not active authentication process for email ({email})")

        auth_obj = result.first()

        status = False
        if auth_obj.code.strip() == code.strip():
            status = True

        # Save status
        auth_obj.status = status
        auth_obj.save()

        # Return status
        if status:
            return True

        raise Exception(f"Code ({code}) is not valid for email {email}")


    def __str__(self):
        return self.email

class Authentication(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now_add=True)
    email = models.ForeignKey('Email', null=False, blank=False, on_delete=models.CASCADE)
    code = models.CharField(max_length=250, null=True, blank=True)
    status = models.BooleanField(null=True, blank=True, help_text='Authentication status')
    ip_address = models.CharField(null=False, blank=False, max_length=250)
    active = models.BooleanField(null=True, blank=True, default=True)

    def reset_all_requests(self):
        Authentication.objects.filter(email=self.email).update(active=False)


    def generate(self):
        # Reset all previous requests
        self.reset_all_requests()
        self.active = True
        self.code = generate_password()
        self.save()

        return self.code

    def send_email(self):
        send(self.email.email, self.code)

    def __str__(self):
        return f"{self.created_date} | {self.email} | {self.code}"
