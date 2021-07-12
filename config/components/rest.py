REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer"
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "utils.authentication.CsrfExemptSessionAuthentication",
        "rest_framework.authentication.BasicAuthentication"
    ],
    "EXCEPTION_HANDLER": "utils.exceptions.custom_exception_handler"
}
