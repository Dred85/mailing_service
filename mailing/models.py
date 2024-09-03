from django.db import models

from users.models import User

NULLABLE = {"null": True, "blank": True}


class Settings(models.Model):
    frequency_tuple = (
        ("daily", "раз в день"),
        ("weekly", "раз в неделю"),
        ("monthly", "раз в месяц"),
    )
    status_tuple = (
        ("завершена", "завершена"),
        ("создана", "создана"),
        ("запущена", "запущена"),
    )
    first_mailing_date = models.DateTimeField(verbose_name="дата первой отправки")
    frequency = models.CharField(
        max_length=150, verbose_name="периодичность", choices=frequency_tuple
    )
    status = models.CharField(
        max_length=150, verbose_name="статус отправки", choices=status_tuple
    )

    message = models.OneToOneField(
        "message.Message",
        on_delete=models.CASCADE,
        verbose_name="сообщение",
        **NULLABLE,
    )
    client = models.ManyToManyField("client.Client", verbose_name="клиент", **NULLABLE)

    is_active = models.BooleanField(default=True, verbose_name="активна")

    owner = models.ForeignKey(
        User,
        verbose_name="владелец",
        help_text="Укажите владельца рассылки",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return f"{self.first_mailing_date}"

    class Meta:
        verbose_name = "настройки"
        verbose_name_plural = "настройки"
        permissions = [
            ("can_disabled_mailing", "can_disabled_mailing"),
        ]


class Attempt(models.Model):
    status_tuple = (
        ("успешно", "успешно"),
        ("не успешно", "не успешно"),
    )
    last_attempt_date = models.DateTimeField(
        auto_now_add=True, verbose_name="дата последней попытки"
    )
    status = models.CharField(
        max_length=150, verbose_name="статус попытки", choices=status_tuple, **NULLABLE
    )
    server_response = models.CharField(
        max_length=150, verbose_name="ответ почтового сервера", **NULLABLE
    )

    mailing = models.ForeignKey(
        Settings, on_delete=models.CASCADE, verbose_name="рассылка"
    )

    def __str__(self):
        return f"{self.last_attempt_date}"

    class Meta:
        verbose_name = "попытка"
        verbose_name_plural = "попытки"
