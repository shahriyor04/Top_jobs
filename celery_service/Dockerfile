FROM python:3.10

WORKDIR /app

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Копируем исходный код проекта
COPY . ./

CMD ["celery", "-A", "root.celery_app", "worker", "--loglevel=info"]