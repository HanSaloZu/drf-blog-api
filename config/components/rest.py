REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication"
    ),
    "EXCEPTION_HANDLER": "utils.exceptions.custom_exception_handler",
    "TEST_REQUEST_DEFAULT_FORMAT": "json"
}
