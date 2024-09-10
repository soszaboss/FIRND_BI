from django.conf import settings
from django.core.mail import send_mail
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv()

def send_otp_via_mail(otp_code, mail_address):
    """Envoyer le code OTP par mail."""
    mail_subject = "Votre Code OTP"
    mail_message = f"Connectez-vous avec ce code : {otp_code}. Il expirera dans 10 minutes dès la réception de ce mail."
    try:
        send_mail(mail_subject, mail_message, settings.EMAIL_HOST_USER, [mail_address])
    except Exception as e:
        print(f"Erreur lors de l'envoi du mail: {e}")

def send_opt_via_sms(otp_code, phone_number):
    """Envoyer le code OTP par SMS via Twilio."""
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    try:
        client.messages.create(
            body=f"Connectez-vous avec ce code : {otp_code}. Il expirera dans 10 minutes dès la réception de ce message.",
            from_=os.environ.get("TWILIO_FROM_NUMBER"),
            to=f"{phone_number}",
        )
    except Exception as e:
        print(f"Erreur lors de l'envoi du SMS: {e}")
