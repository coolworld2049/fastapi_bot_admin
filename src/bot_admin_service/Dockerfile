FROM python:3.11

RUN apt-get update && apt-get upgrade -y && apt-get clean

COPY bot_admin_service/requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r /app/requirements.txt -U

COPY bot_admin_service /app

RUN chmod +x /app/prestart.sh && chmod +x /app/start.sh

ENV PYTHONPATH=/app

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

EXPOSE 80

ENTRYPOINT  ["bash", "./start.sh"]
