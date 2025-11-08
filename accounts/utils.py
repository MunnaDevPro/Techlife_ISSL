# accounts/utils.py
from django.core.mail import send_mail
from django.conf import settings

def send_verification_code_email(user, code, purpose="verify"):
    if purpose == "verify":
        subject = "Verify Your Account"
        message = f"Hello {user.first_name},\n\nYour verification code is: {code}\n\nUse this code to verify your account."
    else:
        subject = "Password Reset Code"
        message = f"Hello {user.first_name},\n\nYour password reset code is: {code}\n\nUse this to reset your password."

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
