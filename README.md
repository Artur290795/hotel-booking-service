# Hotel Booking Service

REST API для управления гостиничными номерами и бронированиями.

## Стек

* Python 3.13
* Django
* Django REST Framework
* PostgreSQL
* Poetry
* Docker / Docker Compose
* Pydantic Settings
* Loguru
* Pytest
* Ruff
* Pre-commit

## Возможности

API позволяет:

* создавать гостиничные номера;
* получать список номеров;
* сортировать номера по цене или дате создания;
* удалять номера вместе со всеми связанными бронированиями;
* изменять данные номера;
* создавать бронирования;
* проверять пересечение бронирований;
* получать список бронирований конкретного номера;
* удалять бронирования.

## Требования

Для локального запуска без Docker:

* Python 3.13+
* PostgreSQL
* Poetry

Для запуска в контейнерах достаточно:

* Docker
* Docker Compose

## Переменные окружения


Для локального запуска создайте файл `.env` в корне проекта.

Пример конфигурации находится в `.env.example`.


## Запуск с Docker Compose

Запустите приложение:

```bash
docker compose up -d --build
```

После запуска API будет доступен по адресу:

```text
http://localhost:8000
```

Проверить состояние контейнеров:

```bash
docker compose ps
```

Посмотреть логи:

```bash
docker compose logs web
```

Остановить приложение:

```bash
docker compose down
```

Для остановки контейнеров с удалением volume базы данных:

```bash
docker compose down -v
```

## Локальный запуск

Установите зависимости:

```bash
poetry install
```

Создайте PostgreSQL database и настройте `.env`.

Примените миграции:

```bash
poetry run python manage.py migrate
```

Запустите сервер:

```bash
poetry run python manage.py runserver
```

API будет доступен по адресу:

```text
http://127.0.0.1:8000
```

## API

### Rooms

#### Создать номер

```http
POST /rooms/
```

Пример запроса:

```json
{
  "description": "Standard room with one double bed",
  "price": "5000.00"
}
```

Пример ответа:

```json
{
  "id": 1,
  "description": "Standard room with one double bed",
  "price": "5000.00",
  "created_at": "2026-09-05T12:00:00Z"
}
```

#### Получить список номеров

```http
GET /rooms/
```

По умолчанию номера возвращаются без заданной сортировки.

Сортировка по цене:

```http
GET /rooms/?sort=price&order=asc
```

Сортировка по дате создания:

```http
GET /rooms/?sort=created_at&order=desc
```

Допустимые значения `sort`:

* `price`
* `created_at`

Допустимые значения `order`:

* `asc`
* `desc`

#### Изменить номер

```http
PATCH /rooms/{room_id}/
```

Пример запроса:

```json
{
  "description": "Updated room description",
  "price": "5500.00"
}
```

#### Удалить номер

```http
DELETE /rooms/{room_id}/
```

При удалении номера все связанные с ним бронирования также удаляются.

### Bookings

#### Создать бронирование

```http
POST /bookings/
```

Пример запроса:

```json
{
  "room_id": 1,
  "start_date": "2026-09-10",
  "finish_date": "2026-09-15"
}
```

Пример ответа:

```json
{
  "id": 1
}
```

Даты должны быть переданы в формате `YYYY-MM-DD`.

Дата начала должна быть раньше даты окончания.

Бронирование не может пересекаться с другим бронированием того же номера.

#### Получить бронирования номера

```http
GET /bookings/?room_id=1
```

Бронирования возвращаются в порядке возрастания даты начала.

Пример ответа:

```json
[
  {
    "id": 1,
    "room_id": 1,
    "start_date": "2026-09-10",
    "finish_date": "2026-09-15"
  }
]
```

#### Удалить бронирование

```http
DELETE /bookings/{booking_id}/
```

## Валидация

На уровне API и базы данных предусмотрены ограничения:

* цена номера не может быть отрицательной;
* дата начала бронирования должна быть раньше даты окончания;
* нельзя создать пересекающееся бронирование для одного номера;
* при обращении к несуществующему номеру или бронированию API возвращает `404 Not Found`;
* некорректные параметры сортировки возвращают `400 Bad Request`.

## Тестирование

Для запуска тестов:

```bash
poetry run pytest
```

Для запуска тестов с покрытием:

```bash
poetry run pytest --cov=src --cov-report=term-missing
```

Текущий набор тестов покрывает бизнес-логику приложения на **92%**.

Непокрыты стандартные точки входа Django (`ASGI`/`WSGI`) и конфигурация логирования, поскольку они не содержат бизнес-логики приложения.

## Линтинг и форматирование

Проверка Ruff:

```bash
poetry run ruff check .
```

Проверка форматирования:

```bash
poetry run ruff format --check .
```

Автоматическое форматирование:

```bash
poetry run ruff format .
```

## Pre-commit

Перед коммитом автоматически выполняются:

* проверка Ruff;
* форматирование Ruff;
* тесты.

Установить hooks:

```bash
poetry run pre-commit install
```

Запустить проверки вручную:

```bash
poetry run pre-commit run --all-files
```

## Структура проекта

```text
hotel-booking-service/
├── src/
│   ├── bookings/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── tests/
│   ├── config/
│   │   └── logging.py
│   └── hotel_service/
│       ├── settings.py
│       ├── urls.py
│       ├── asgi.py
│       └── wsgi.py
├── .env.example
├── .gitignore
├── .dockerignore
├── .pre-commit-config.yaml
├── docker-compose.yml
├── Dockerfile
├── manage.py
├── poetry.lock
├── pyproject.toml
└── README.md
```

## Допущения

* Аутентификация и авторизация не реализованы.
* Стоимость номера указывается за одну ночь.
* Валюта стоимости не фиксируется API.
* Бронирование задаётся датами начала и окончания проживания.
* Проверка пересечения бронирований выполняется на уровне приложения.
* Данные хранятся в PostgreSQL.
* Миграции Django используются для управления схемой базы данных.
* API принимает и возвращает данные в формате JSON.
