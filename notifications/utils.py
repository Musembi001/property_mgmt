from django.core.mail import send_mail
from django.conf import settings
import requests

def send_email_notification(user, subject, message):
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

def send_sms_notification(phone_number, message):
    # Example using Africa's Talking or Twilio
    pass  # Implement with your SMS provider

def send_whatsapp_notification(phone_number, message):
    # Example using Twilio WhatsApp API
    pass  # Implement with your WhatsApp provider