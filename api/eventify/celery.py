from __future__ import unicode_literals

import os
from typing import Any

from celery import Celery
from celery.signals import setup_logging
from django.conf import settings

# Set the default Django settings module for the 'celery'.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eventify.settings")
app = Celery("eventify")
app.conf.enable_utc = True
# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object(settings, namespace="CELERY")


@setup_logging.connect
def config_loggers(*args: Any, **kwargs: Any) -> None:
    from logging.config import dictConfig

    from django.conf import settings

    dictConfig(settings.LOGGING)
