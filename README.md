# HabitTracker

## Описание проекта

Habit Tracker — это веб-приложение, разработанное на Django с использованием Poetry для управления зависимостями. Приложение позволяет пользователям создавать, отслеживать и управлять привычками, а также получать напоминания через Telegram. Привычки делятся на полезные и приятные, с возможностью настройки вознаграждений, периодичности и публичности.

## Основные функции

- **Создание и управление привычками**: пользователи могут создавать привычки, указывая место, время, действие, периодичность и вознаграждение.
- **Интеграция с Telegram**: отправка напоминаний о выполнении привычек через отложенные задачи.

## Установка и настройка

### Требования

- Python 3.8+
- Django 5.2
- Django REST Framework 3.16
- Poetry
- PostgreSQL
- Redis (для Celery)

### Установка

1. **Клонируйте репозиторий**:
   ```bash
   git clone <repository_url>
   cd habit_tracker
   ```

2. **Установите Poetry** (если не установлено):
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

3. **Инициализируйте зависимости**:
   ```bash
   poetry install
   ```

4. **Активируйте виртуальное окружение**:
   ```bash
   poetry env activate
   ```

5. **Настройте базу данных PostgreSQL**:
   ```bash
   brew install postgresql
   createdb habit_tracker_db
   ```

6. **Настройте переменные окружения**:
   Создайте файл `.env` в корне проекта:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/habit_tracker_db
   SECRET_KEY=your_django_secret_key
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token
   REDIS_URL=redis://localhost:6379/0
   ```

7. **Примените миграции**:
   ```bash
   python manage.py migrate
   ```

8. **Запустите сервер**:
   ```bash
   python manage.py runserver
   ```

9. **Запустите Celery для обработки отложенных задач**:
   ```bash
   celery -A habit_tracker worker -l info
   celery -A habit_tracker beat -l info
   ```


