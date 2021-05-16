REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": "utils.handlers.custom_exception_handler",
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "utils.authentication.CsrfExemptSessionAuthentication",
        "rest_framework.authentication.BasicAuthentication"
    )
}
