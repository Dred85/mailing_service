from django.db import models


class Message(models.Model):
    subject = models.CharField(max_length=150, verbose_name='тема письма')
    text = models.TextField(verbose_name='текст сообщения')

    def __str__(self):
        return f'{self.subject}'

    class Meta:
        verbose_name = 'сообщение'
        verbose_name_plural = 'сообщения'