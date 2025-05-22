FROM python:3.9-slim

# Обновим pip и установим системные зависимости
RUN apt-get update && apt-get install -y \
    build-essential \
    && pip install --upgrade pip \
    && apt-get clean

WORKDIR /app

# Скопировать зависимости и установить их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Скопировать весь проект
COPY . .

CMD ["python", "app/bot.py"]
