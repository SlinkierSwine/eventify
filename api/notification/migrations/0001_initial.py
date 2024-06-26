# Generated by Django 5.0.6 on 2024-06-24 12:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('event', '0003_event_notify_before_minutes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('message', models.TextField(verbose_name='message')),
                ('provider', models.CharField(choices=[('telegram', 'Telegram'), ('vk', 'Vk'), ('email', 'Email'), ('web', 'Web')], max_length=128, verbose_name='provider')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifications', to='event.event')),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_notifications', to='event.eventparticipant')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
