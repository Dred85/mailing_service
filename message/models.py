from django.db import models

from users.models import User


class Message(models.Model):
    subject = models.CharField(max_length=150, verbose_name="тема письма")
    text = models.TextField(verbose_name="текст сообщения")
    owner = models.ForeignKey(
        User,
        verbose_name="владелец",
        help_text="Укажите владельца сообщения",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        verbose_name = "сообщение"
        verbose_name_plural = "сообщения"
        permissions = [
            ("can_view_subject_message", "can_view_subject_message"),
            ("can_view_text_message", "can_view_text_message"),
        ]

    def __str__(self):
        return f"{self.subject}"
