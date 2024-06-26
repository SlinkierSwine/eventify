from __future__ import unicode_literals

# This ensures that the app is loaded when Django starts
from eventify.celery import app as celery_app

__all__ = ("celery_app",)
