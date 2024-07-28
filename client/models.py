from django.db import models

NULLABLE = {'null': True, 'blank': True}


class Client(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='имя')
    last_name = models.CharField(max_length=150, verbose_name='фамилия')
    email = models.EmailField(verbose_name='почта', unique=True)
    comment = models.TextField(verbose_name='комментарий')

    def __str__(self):
        return f'{self.email} ({self.first_name} {self.last_name})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'