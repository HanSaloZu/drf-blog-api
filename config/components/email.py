EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = environ["EMAIL_HOST_USER"]
EMAIL_HOST_PASSWORD = environ["EMAIL_HOST_PASSWORD"]
