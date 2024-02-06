FROM python:3.10-slim-buster


WORKDIR /app

# Устанавливаем зависимости
COPY celery_service/requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код проекта
COPY . ./

# Устанавливаем переменные окружения для Django
#ENV DJANGO_SETTINGS_MODULE=root.settings.application

# Запускаем миграции и Gunicorn
#CMD python manage.py makemigrations
#CMD python manage.py migrate
#CMD python manage.py collectstatic --noinput
##CMD python manage.py runserver 0.0.0.0:8000
#CMD gunicorn root.wsgi:application --bind 0.0.0.0:8000
