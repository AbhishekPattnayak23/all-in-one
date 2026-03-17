from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def send_reset_email_task(email: str, reset_link: str):
    subject = "Reset your password"
    message = f"Please click the link to reset your password: {reset_link}"
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [email])
