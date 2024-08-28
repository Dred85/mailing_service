import datetime
from datetime import timedelta
from time import strftime


from django.conf import settings
from django.core.mail import send_mail

# Импортирую свою почту
from dotenv import load_dotenv
import os

from mailing.models import Settings

load_dotenv()


def send_mailing():
    # Получаю все рассылки
    mailings = Settings.objects.all()

    # Запускаю цикл по рассылкам, где получаю данные и запускаю отправку сообщений
    for send_mail_for_customers in mailings:

        # Узнаю надо ли отправить рассылку в данный момент цикла
        if send_mail_for_customers.mailing_start_date <= datetime.date.today() <= send_mail_for_customers.mailing_end_date:

            # Получаю название рассылки
            subject_of_letter = send_mail_for_customers.message.subject_of_letter
            # Получаю текст сообщения
            message = send_mail_for_customers.message.body_of_letter
            # Получаю клиентов которым надо отправить сообщение
            mails = send_mail_for_customers.customers_of_service.all()

            # Если рассылка отправляется впервые, то заполняю дату первой отправки и ставлю дату следующей отправки в
            # зависимости от её периодичности отправки
            if not send_mail_for_customers.date_and_time_of_first_mailing:
                send_mail_for_customers.date_and_time_of_first_mailing = strftime('%Y-%m-%d %H:%M:%S')

                # Если рассылку надо отправлять каждый день
                if str(send_mail_for_customers.periodicity) == 'Раз в день':
                    send_mail_for_customers.date_letter_was_sent = datetime.date.today() + timedelta(days=1)
                    send_mail_for_customers.save()

                # Если рассылку надо отправлять каждую неделю
                elif str(send_mail_for_customers.periodicity) == 'Раз в неделю':
                    send_mail_for_customers.date_letter_was_sent = datetime.date.today() + timedelta(days=7)
                    send_mail_for_customers.save()

                # Если рассылку надо отправлять каждый месяц
                else:
                    send_mail_for_customers.date_letter_was_sent = datetime.date.today() + timedelta(days=30)
                    send_mail_for_customers.save()

                # Отправляю рассылки
                for mailing in mails:
                    send_mail(
                        subject=subject_of_letter,
                        message=message,
                        from_email=os.getenv('mail'),
                        recipient_list=[mailing]
                    )

            # Если рассылка отправляется не первый раз, то смотрю дату следующей рассылки, которую установил выше,
            # сравниваю с часом в который необходимо отправить рассылку и с минутой в которую необходимо отправить
            # рассылку
            elif send_mail_for_customers.date_letter_was_sent == datetime.date.today() and str(send_mail_for_customers.time_which_newsletter_sent) == str(strftime('%H')) and str(send_mail_for_customers.minute_when_newsletter_should_sent) == str(strftime('%M')):

                # Если рассылку надо отправлять каждый день
                if str(send_mail_for_customers.periodicity) == 'Раз в день':
                    send_mail_for_customers.date_letter_was_sent = datetime.date.today() + timedelta(days=1)
                    send_mail_for_customers.save()

                # Если рассылку надо отправлять каждую неделю
                elif str(send_mail_for_customers.periodicity) == 'Раз в неделю':
                    send_mail_for_customers.date_letter_was_sent = datetime.date.today() + timedelta(days=7)
                    send_mail_for_customers.save()

                # Если рассылку надо отправлять каждый месяц
                else:
                    send_mail_for_customers.date_letter_was_sent = datetime.date.today() + timedelta(days=30)
                    send_mail_for_customers.save()

                # Отправляю рассылку пользователям
                for mailing in mails:
                    send_mail(
                        subject=subject_of_letter,
                        message=message,
                        from_email=os.getenv('mail'),
                        recipient_list=[mailing]
                    )