# url_shortener

http сервис для сокращения url
- UI реализован с помощью **Swagger (drf-spectacular)**;
- Регистрация, авторизация по **jwt токену**;
- Реализовано создание, редактирование и удаление сокращенных url пользователя, получение всех сокращенных url. Пользователь может задать кастомное сокращение ссылки, при отправке пустого поля сокращение будет сгенерированно;
- Фильтрация, сортировка и пагинация в комплекте с проверкой валидности ссылки и существования странички;
- Скриншот происходит автоматически при сохранении url при помощи **pyppeteer** + **celery** + **redis**;


# Запуск

#### `docker-compose up --build`

> Важно! В проекте реализован автоматический скриншот с помощью pyppeteer (и, соответственно, celery + redis), в котором иногда возникает проблема с совместимостью **importlib-metadata**. Будет обидно если у вас не запустится из-за этого бага, в этом случае буду готов все показать с личной машины (тестил на ubuntu 20.04 lts)
https://stackoverflow.com/questions/74025035/importerror-cannot-import-name-celery-from-celery

> При первом обращении к pyppeteer ему нужно будет установить ~150MB хромиума