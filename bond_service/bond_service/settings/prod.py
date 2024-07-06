import os
import sys
from datetime import timedelta

from .base import *  # noqa

SIMPLE_JWT = {"ACCESS_TOKEN_LIFETIME": timedelta(minutes=30)}

ALLOWED_HOSTS += os.getenv("PROD_URL").split()  # noqa

# trusted origins for rest framework (using django-cors-headers)
CORS_ALLOWED_ORIGINS = os.getenv("CORS_URL").split()
# trusted origins for django admin
CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS").split()
CSRF_COOKIE_SECURE = True

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler", "stream": sys.stderr}},  # noqa
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "ERROR",  # change debug level as appropriate
            "propagate": True,
        }
    },
}

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = ("rest_framework.renderers.JSONRenderer",)  # noqa
