import smtplib
from datetime import datetime, timedelta

from config import settings

from django.core.mail import send_mail
from mailing.models import Settings, Attempt


def send_mailing_email(mailing_item: Settings, selected_clients):
    """Отправка сообщения клиентам"""
    for client in selected_clients:
        try:
            send_mail(
                subject=mailing_item.message.text,  # Использую текст сообщения в качестве темы
                message=mailing_item.message.text,  # Тело сообщения
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[client.email],
                fail_silently=False,
            )

            attempt = Attempt.objects.create(status="успешно", mailing=mailing_item)

        except smtplib.SMTPException as e:
            attempt = Attempt.objects.create(
                status="не успешно", mailing=mailing_item, server_response=e
            )

        attempt.save()
        mailing_item.status = "запущена"
        mailing_item.save()


def handle_mailing(mailing, selected_clients):
    send_mailing_email(mailing, selected_clients)  # Передаю клиента в функцию
    days_count = 1
    if mailing.frequency == "daily":
        days_count = 1
    elif mailing.frequency == "weekly":
        days_count = 7
    elif mailing.frequency == "monthly":
        days_count = 30
    mailing.first_mailing_date += timedelta(days=days_count)
    mailing.save()


def send_mailing_scheduled():
    """Отправка сообщений по расписанию"""
    now = datetime.now()
    before = now + timedelta(minutes=5)
    after = now - timedelta(minutes=5)
    mailing_list_first_attempt = Settings.objects.filter(first_mailing_date__lt=now)

    for m in mailing_list_first_attempt:
        if not Attempt.objects.filter(mailing=m).exists():
            handle_mailing(m)

    mailing_list = Settings.objects.filter(
        first_mailing_date__lt=before, first_mailing_date__gt=after
    )

    for mailing in mailing_list:
        handle_mailing(mailing)
