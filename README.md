# 🏦 SITEWALLETS - API сервис для управления кошельками

![Django](https://img.shields.io/badge/Django-5.2-092E20?logo=django)
![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-4169E1?logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?logo=docker)

**SITEWALLETS** — это REST API сервис для управления пользовательскими кошельками.

## 📋 Оглавление

- [🚀 Быстрый старт](#section-bystryj-start)
- [🔌 API Endpoints](#section-api-endpoints)
- [🔧 Технологический стек](#section-tehnologicheskij-stek)
- [📁 Структура проекта](#section-struktura-proekta)
- [⚡ Конкурентность и безопасность транзакций](#section-konkurentnost-tranzakcij)
- [🧪 Тестирование](#section-testirovanie)
- [🖥️ Интерфейсы](#section-interfejsy)
- [📊 Adminer - Управление БД](#section-adminer)
- [👨‍💻 Автор](#section-avtor)

<a id="section-bystryj-start"></a>
## 🚀 Быстрый старт

Для запуска проекта необходим запущенный **Docker Desktop**

```bash
# Клонировать репозиторий
git clone https://github.com/MihailTarbeev/Wallets.git
cd Wallets

# Запустить все сервисы
docker compose up --build
```

После запуска будут доступны:

API: http://127.0.0.1:8000

Adminer (управление БД): http://127.0.0.1:8080
<a id="section-api-endpoints"></a>
## 🔌 API Endpoints

### 📋 Основные эндпоинты

| Метод | Endpoint | Описание |
|-------|----------|----------|
| `GET` | `/api/v1/wallets/` | Получить список всех кошельков |
| `POST` | `/api/v1/wallets/` | Создать новый кошелек |
| `GET` | `/api/v1/wallets/<uuid:pk>/` | Получить баланс конкретного кошелька |
| `POST` | `/api/v1/wallets/<uuid:pk>/operation/` | Выполнить операцию (пополнение/списание) |
| `GET` | `/api/v1/operations/` | Получить историю всех операций |

### 💰 Примеры запросов
___
GET `http://127.0.0.1:8000/api/v1/wallets/`

Пример успешного ответа:
```json
[
    {
        "uuid": "ae9ce189-0353-47a6-bf78-4fd0c1bac642",
        "balance": "201.00"
    },
    {
        "uuid": "4197e0a8-8310-4234-858c-0166d10ed916",
        "balance": "777.00"
    }
]
```
___
POST `http://127.0.0.1:8000/api/v1/wallets/`

Тело запроса:
```json
{"balance": 500} 
```
Пример успешного ответа:
```json
{
    "uuid": "dab85512-ff01-41f0-9d53-af886e278514",
    "balance": "500.00"
}
```
___
GET `http://127.0.0.1:8000/api/v1/wallets/ae9ce189-0353-47a6-bf78-4fd0c1bac642`

Пример успешного ответа:
```json
{
    "uuid": "ae9ce189-0353-47a6-bf78-4fd0c1bac642",
    "balance": "201.00"
}
```
___
POST `http://127.0.0.1:8000/api/v1/wallets/ae9ce189-0353-47a6-bf78-4fd0c1bac642/operation`

Тело запроса:
```json
{
    "operation_type": "DEPOSIT",
    "amount": 333
}
```

Пример успешного ответа:
```json
{
    "wallet": {
        "uuid": "ae9ce189-0353-47a6-bf78-4fd0c1bac642",
        "balance": "534.00",
        "updated_at": "2025-12-09T16:30:03.634419+00:00"
    },
    "operation": {
        "transaction_id": "47a52983-021a-44d4-90a3-e611c226c7f8",
        "operation_type": "DEPOSIT",
        "amount": "333.00",
        "created_at": "2025-12-09T16:30:03.625865+00:00"
    }
}
```
___
POST `http://127.0.0.1:8000/api/v1/wallets/ae9ce189-0353-47a6-bf78-4fd0c1bac642/operation`

Тело запроса:
```json
{
    "operation_type": "WITHDRAW",
    "amount": 700
}
```

Пример успешного ответа:
```json
{
    "wallet": {
        "uuid": "ae9ce189-0353-47a6-bf78-4fd0c1bac642",
        "balance": "434.00",
        "updated_at": "2025-12-09T16:31:32.492564+00:00"
    },
    "operation": {
        "transaction_id": "0c1deae1-979b-4a70-93c1-eebe3c19184c",
        "operation_type": "WITHDRAW",
        "amount": "100.00",
        "created_at": "2025-12-09T16:31:32.490284+00:00"
    }
}
```
___
GET `http://127.0.0.1:8000/api/v1/operations/`

Пример успешного ответа:
```json
[
    {
        "created_at": "2025-12-09T19:31:32.490284+03:00",
        "wallet": "ae9ce189-0353-47a6-bf78-4fd0c1bac642",
        "operation_type": "WITHDRAW",
        "amount": "100.00",
        "transaction_id": "0c1deae1-979b-4a70-93c1-eebe3c19184c"
    },
    {
        "created_at": "2025-12-09T19:30:03.625865+03:00",
        "wallet": "ae9ce189-0353-47a6-bf78-4fd0c1bac642",
        "operation_type": "DEPOSIT",
        "amount": "333.00",
        "transaction_id": "47a52983-021a-44d4-90a3-e611c226c7f8"
    }
]
```
<a id="section-tehnologicheskij-stek"></a>
## 🔧 Технологический стек
Основные технологии:

- Python 3.12 - основной язык разработки

- Django 5.2.9 - веб-фреймворк

- Django REST Framework 3.16.1 - REST API

- PostgreSQL 17 - база данных

- Docker & Docker Compose - контейнеризация

Дополнительные зависимости:

- psycopg2-binary - драйвер PostgreSQL

- pytest + pytest-django - тестирование

- pytest-cov - покрытие кода

- adminer - веб-интерфейс для БД

<a id="section-struktura-proekta"></a>
## 📁 Структура проекта
```
sitewallets/
├── sitewallets/                 # Основной проект Django
│   ├── __init__.py
│   ├── settings.py              # Настройки проекта
│   ├── urls.py                  # Маршрутизация
│   └── wsgi.py & asgi.py        # WSGI/ASGI конфигурации
├── wallets/                     # Приложение для работы с кошельками
│   ├── migrations/              # Миграции базы данных
│   ├── tests/                   # Тесты
│   │   ├── conftest.py          # Файл с фикстурами для pytest
│   │   ├── test_models.py
│   │   ├── test_views.py
│   │   ├── test_serializers.py
│   │   └── test_integration.py
│   ├── models.py               # Модели Wallet и Operation
│   ├── views.py                # APIView-классы
│   ├── serializers.py          # Сериализаторы
│   └── urls.py                 # Маршрутизация приложения
├── Dockerfile                  # Docker-образ приложения
├── db.json                     # Тестовые данные
├── entrypoint.sh               # Скрипт инициализации
├── manage.py                   
├── pytest.ini                  # Конфигурация pytest
├── requirements.txt            # Зависимости Python
.env                            # Файл тестовой конфигурации
compose.yml                     # Файл конфигурации Docker compose
```
<a id="section-konkurentnost-tranzakcij"></a>
## ⚡ Конкурентность и безопастность транзакций

Защита от race conditions:
Для гарантии корректной работы при параллельных запросах реализована система блокировок на уровне строк БД:

```python
with transaction.atomic():
    # Блокируем запись кошелька для других транзакций
    wallet = Wallet.objects.select_for_update(nowait=False).get(uuid=pk)
    
    if operation_type == 'WITHDRAW' and wallet.balance < amount:
        return Response({"error": "Insufficient funds"}, status=400)
    
    # Выполняем операцию
    if operation_type == 'DEPOSIT':
        wallet.balance += amount
    else:
        wallet.balance -= amount
    
    wallet.save()
```
<a id="section-testirovanie"></a>
## 🧪 Тестирование

```bash
Запуск тестов:
# 1. Сначала запустите проект
docker compose up -d

# 2. Запустите тесты в контейнере
docker compose exec sitewallets pytest

```
<a id="section-interfejsy"></a>
## 🖥️ Интерфейсы

JSON API (по умолчанию):
API возвращает данные в формате JSON. Для включения браузерного интерфейса Django REST Framework в settings.py:
```python
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        'rest_framework.renderers.JSONRenderer',
        # 'rest_framework.renderers.BrowsableAPIRenderer'  # ← раскомментировать
    ]
}
```
<a id="section-adminer"></a>
## 📊 Adminer

Для удобного управления базой данных подключен Adminer:

URL: http://127.0.0.1:8080

Данные для подключения к БД можно взять из файла конфигурации .env

<a id="section-avtor"></a>
## 👨‍💻 Автор

**Михаил Тарбеев**<br>
Python Backend Developer

GitHub: https://github.com/MihailTarbeev

