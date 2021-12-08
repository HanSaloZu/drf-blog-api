EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = environ["EMAIL_HOST"]

EMAIL_PORT = int(environ["EMAIL_PORT"])

EMAIL_USE_TLS = bool(int(environ["EMAIL_USE_TLS"]))

EMAIL_HOST_USER = environ["EMAIL_HOST_USER"]

EMAIL_HOST_PASSWORD = environ["EMAIL_HOST_PASSWORD"]

EMAIL_VERIFICATION_CODE_LIFETIME = timedelta(minutes=15)
