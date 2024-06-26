# Generated by Django 5.0.6 on 2024-06-16 21:35

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventparticipant',
            name='anonymous_participant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='participating_events', to='event.anonymousparticipant'),
        ),
        migrations.AlterField(
            model_name='eventparticipant',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='participating_events', to=settings.AUTH_USER_MODEL),
        ),
    ]
