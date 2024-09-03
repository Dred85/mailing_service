import datetime
from django import template

import random
import string

from django.utils.html import conditional_escape
from django.utils.safestring import mark_safe

from blog.models import Blog
from client.models import Client
from mailing.models import Settings

register = template.Library()


# Создание тега
@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)


@register.simple_tag
def count_mailing():
    """Подсчет общего количества рассылок"""
    count_mailing_ = Settings.objects.count()
    return f"Количество рассылок сейчас: {count_mailing_}"


@register.simple_tag
def count_mailing_activ():
    """Подсчет количества активных рассылок"""
    count_mailing_activ_ = Settings.objects.filter(is_active=True).count()
    return f"Количество активных рассылок сейчас: {count_mailing_activ_}"


@register.simple_tag
def count_clients_uniq():
    """Подсчет количества уникальных клиентов для рассылок"""
    count_clients_uniq_ = Client.objects.values("email").distinct().count()
    return f"Количество уникальных клиентов для рассылок: {count_clients_uniq_}"


@register.simple_tag
def get_random_3_blogs():
    """Возвращает три случайные статьи из блога."""
    all_blogs = list(Blog.objects.all())
    if len(all_blogs) < 3:
        return all_blogs  # Возвращаем все статьи, если их меньше трех

    random_blogs_list = random.sample(all_blogs, 3)
    return random_blogs_list


# Создание фильтра
@register.filter(needs_autoescape=True)
def initial_letter_filter(text, autoescape=True):
    first, other = text[0], text[1:]
    if autoescape:
        esc = conditional_escape
    else:
        esc = lambda x: x
    result = "<strong>%s</strong>%s" % (esc(first), esc(other))
    return mark_safe(result)


# Создание тега
@register.simple_tag
def generate_fake_mail(length: int = "10"):
    # length = int(s_length)
    letters = string.ascii_letters + string.digits  # + string.punctuation
    mail = "".join(random.choice(letters) for _ in range(length))

    letters2 = string.ascii_lowercase
    mail2 = "".join(random.choice(letters2) for _ in range(length // 2))
    return f"{mail}@{mail2}.com"


@register.filter()
def media_filter(path):
    if path:
        return f"/media/{path}"

    return "/static/image/no_image.png"


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


# @register.filter
# def get_random_3_blogs(query_set):
#     """Возвращает три случайные статьи из блога."""
#
#     # Получаем все статьи
#     all_blogs = query_set
#     # Проверяем, достаточно ли статей
#     if len(all_blogs) < 3:
#         return all_blogs  # Возвращаем все статьи, если их меньше трех
#
#     # Выбираем три случайные статьи
#     random_blogs_list = random.sample(all_blogs, 3)
#
#     return f" три случайные блога {random_blogs_list}"
