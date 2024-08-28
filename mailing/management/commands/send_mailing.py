from django.core.management import BaseCommand


from mailing.tasks import send_mailing


class Command(BaseCommand):
    """Кастомная команда для рассылки данных по почте"""

    def handle(self, *args, **options):
        """Соответственно метод для рассылки данных по почте"""
        send_mailing()