from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_email(subject,email_text,EMAIL_HOST_USER,to_email):
    send_mail(subject,email_text,EMAIL_HOST_USER,[to_email],fail_silently=False)
