FROM python:3.13-slim

# Установим зависимости для pip, curl и автообновления кода
RUN apt-get update && apt-get install -y \
    curl \
    inotify-tools \
    && rm -rf /var/lib/apt/lists/*

# Создаём рабочую директорию
WORKDIR /code

# Копируем зависимости
COPY requirements.txt ./

# Устанавливаем зависимости
RUN python -m venv .venv && \
    .venv/bin/pip install --upgrade pip && \
    .venv/bin/pip install -r requirements.txt && \
    .venv/bin/pip install watchdog

# Копируем исходный код
COPY ./app ./app

# Запуск приложения с автообновлением при изменениях в .py файлах
CMD [".venv/bin/watchmedo", "auto-restart", "--directory=./app", "--pattern=*.py", "--recursive", "--", ".venv/bin/python", "app/main.py"]
