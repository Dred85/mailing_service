# Generated by Django 4.2 on 2024-08-25 03:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("message", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="message",
            options={
                "permissions": [
                    ("can_edit_subject", "can_edit_subject"),
                    ("can_edit_text", "can_edit_text"),
                ],
                "verbose_name": "сообщение",
                "verbose_name_plural": "сообщения",
            },
        ),
        migrations.AddField(
            model_name="message",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                help_text="Укажите владельца сообщения",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
                verbose_name="владелец",
            ),
        ),
    ]
