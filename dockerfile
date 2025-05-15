
FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y cron && \
    apt-get clean

COPY . .

RUN chmod +x /app/backups/backup.sh

COPY cronjobs /etc/cron.d/backup-cron

RUN chmod 0644 /etc/cron.d/backup-cron && \
    crontab /etc/cron.d/backup-cron


RUN touch /var/log/cron.log

RUN apt-get update && apt-get install -y postgresql-client && apt-get clean

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD cron && python manage.py runserver 0.0.0.0:8000
