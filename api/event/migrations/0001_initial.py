# Generated by Django 5.0.6 on 2024-06-16 19:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AnonymousParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('social_contact', models.CharField(help_text='Id of social account', max_length=256, verbose_name='social contact')),
                ('notification_provider', models.CharField(choices=[('telegram', 'Telegram'), ('vk', 'Vk'), ('email', 'Email'), ('web', 'Web')], max_length=128, verbose_name='notification provider')),
            ],
            options={
                'verbose_name': 'AnonymousParticipant',
                'verbose_name_plural': 'AnonymousParticipants',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='created at')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='updated at')),
                ('name', models.CharField(max_length=256, verbose_name='name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('start_datetime', models.DateTimeField(verbose_name='start datetime')),
                ('end_datetime', models.DateTimeField(verbose_name='end datetime')),
                ('is_canceled', models.BooleanField(default=False, verbose_name='is canceled')),
                ('is_private', models.BooleanField(default=False, verbose_name='is private')),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='created_events', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Event',
                'verbose_name_plural': 'Events',
            },
        ),
        migrations.CreateModel(
            name='EventParticipant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anonymous_participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participating_events', to='event.anonymousparticipant')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participants', to='event.event')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participating_events', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
