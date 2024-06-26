# Generated by Django 5.0.6 on 2024-06-26 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_event_notify_before_minutes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anonymousparticipant',
            name='notification_provider',
            field=models.CharField(choices=[('email', 'Email'), ('web', 'Web'), ('vk', 'Vk'), ('google', 'Google'), ('telegram', 'Telegram')], max_length=128, verbose_name='notification provider'),
        ),
    ]