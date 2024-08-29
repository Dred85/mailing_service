Система управления Email-рассылками: Cизый Голубь
Обзор
Система Email-рассылок — это приложение на Django для управления и отправки email-кампаний. Это приложение позволяет создавать и управлять списками рассылок, составлять сообщения и планировать отправку писем с различными интервалами.

Возможности
Управление клиентами: Хранение и управление данными клиентов.
Создание сообщений: Составление и хранение email-сообщений.
Списки рассылок: Создание и управление email-кампаниями, настройка интервалов отправки.
Автоматическая отправка: Автоматическая отправка писем на основе расписания.
Ручной запуск: Ручной запуск рассылок через командную строку.
Логирование и мониторинг: Отслеживание попыток отправки и их статусов.
Содержание
Установка
Использование
Запуск периодических задач
Командная строка
Установка
Клонируйте репозиторий:

git clone https://github.com/вашпользователь/email-mailing-system.git
cd email-mailing-system
Создайте виртуальное окружение:

python -m venv env
source env/bin/activate   # На Windows используйте `env\Scripts\activate`
Установите зависимости:

pip install -r requirements.txt
Создайте файл переменных окружения:

В корневой директории проекта скопируйте файл .env.sample в .env и заполните переменные окружения:

Примените миграции:

python manage.py migrate
Создайте суперпользователя (по желанию):

python manage.py csu
Использование
Запуск сервера разработки:

python manage.py runserver
Доступ к админ-панели:

Перейдите по адресу http://127.0.0.1:8000/admin и войдите с учетными данными суперпользователя.

Создание и управление рассылками:

Добавьте клиентов через админ-панель или создайте их через оболочку Django.
Составьте сообщения и создайте списки рассылок.
Запланируйте рассылки и проверьте статус email-кампаний.
Запуск периодических задач
В системе используется библиотека: django-crontab  для обработки периодических задач.

Запуск планировщика задач:
python manage.py crontab add

