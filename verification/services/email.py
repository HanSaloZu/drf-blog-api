from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from ..tokens import confirmation_token
from .activation import generate_uidb64, generate_profile_activation_url


def send_email(email_subject, email_template, email_context, to_email):
    message = render_to_string(email_template, email_context)
    email = EmailMessage(
        email_subject, message, to=[to_email]
    )
    email.send()


def send_profile_activation_email(user):
    token = confirmation_token.make_token(user)
    uidb64 = generate_uidb64(user)
    url = generate_profile_activation_url(token, uidb64)

    email_context = {
        "user": user,
        "url": url
    }

    send_email("Activate your profile", "email/activate_profile.html",
               email_context, user.email)
