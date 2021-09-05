from django.template.loader import render_to_string
from django.core.mail import EmailMessage


def send_email(email_subject, email_template, email_context, to_email):
    message = render_to_string(email_template, email_context)
    email = EmailMessage(
        email_subject, message, to=[to_email]
    )
    email.send()


def send_verification_email(user, verification_code):
    email_context = {
        "user": user,
        "code": verification_code
    }

    send_email("Verify your email", "email/verify_email.html",
               email_context, user.email)
