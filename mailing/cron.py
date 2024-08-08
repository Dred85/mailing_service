import smtplib
from datetime import datetime, timedelta

from django.core.mail import send_mail

from config import settings
from mailing.models import Settings, Attempt


def send_mailing_email(mailing_item: Settings):
    try:
        send_mail(
            f'{mailing_item.message}',
            f'{mailing_item.message.text}',
            settings.EMAIL_HOST_USER,
            recipient_list=[client.email for client in mailing_item.client.all()],
            fail_silently=False,
        )
        attempt = Attempt.objects.create(status='успешно', mailing=mailing_item)
    except smtplib.SMTPException as e:
        attempt = Attempt.objects.create(status='не успешно', mailing=mailing_item, server_response=e)
    attempt.save()
    mailing_item.status = 'запущена'
    mailing_item.save()


def handle_mailing(mailing):
    send_mailing_email(mailing)
    days_count = 1
    if mailing.frequency == 'daily':
        days_count = 1
    elif mailing.frequency == 'weekly':
        days_count = 7
    elif mailing.frequency == 'monthly':
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

    mailing_list = Settings.objects.filter(first_mailing_date__lt=before,
                                           first_mailing_date__gt=after)

    for mailing in mailing_list:
        handle_mailing(mailing)
