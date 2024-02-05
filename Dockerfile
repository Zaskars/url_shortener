FROM python:3.8-slim

# Установите необходимые системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    firefox-esr \
    wget \
    && rm -rf /var/lib/apt/lists/* \
    && wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz \
    && tar -xvzf geckodriver* \
    && chmod +x geckodriver \
    && mv geckodriver /usr/local/bin/

# Установите рабочую директорию в контейнере
WORKDIR /app

# Копируйте файлы проекта и файлы зависимостей в контейнер
COPY . /app
COPY requirements.txt /app/

# Установите зависимости Python
RUN pip install --no-cache-dir -r requirements.txt

# Определите команду для запуска приложения
CMD ["gunicorn", "-b", "0.0.0.0:8000", "urlshortener.wsgi:application"]