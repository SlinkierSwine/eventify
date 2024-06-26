from django.db import models


class TimeStampableModel(models.Model):
    created_at = models.DateTimeField("created at", auto_now_add=True)
    updated_at = models.DateTimeField("updated at", auto_now=True)

    class Meta:
        abstract = True
