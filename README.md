# HabitTracker

## Описание проекта

Habit Tracker — это веб-приложение, разработанное на Django с использованием Poetry для управления зависимостями. Приложение позволяет пользователям создавать, отслеживать и управлять привычками, а также получать напоминания через Telegram. Привычки делятся на полезные и приятные, с возможностью настройки вознаграждений, периодичности и публичности.

## Основные функции

- **Создание и управление привычками**: пользователи могут создавать привычки, указывая место, время, действие, периодичность и вознаграждение.
- **Интеграция с Telegram**: отправка напоминаний о выполнении привычек через отложенные задачи.

## 📣 Запуск с Docker Compose

Проект поддерживает запуск в контейнерах с использованием **Docker Compose**, включая:

* Django-приложение
* PostgreSQL
* Redis
* Celery (воркер)
* Celery Beat (планировщик задач)

---

### 📦 Шаги для запуска проекта в Docker

1. Убедитесь, что у вас установлены Docker и Docker Compose.

   * [Установка Docker](https://docs.docker.com/get-docker/)
   * [Установка Docker Compose](https://docs.docker.com/compose/install/)

2. Клонируйте репозиторий:

   ```bash
   git clone https://github.com/yourusername/LearnCoreAPI.git
   cd LearnCoreAPI
   ```

3. Создайте файл `.env`:

   ```bash
   cp .env.example .env
   ```

   Затем отредактируйте `.env`, указав переменные окружения (настройки БД, секретный ключ, параметры Redis и др.).

4. Запустите проект:

   ```bash
   docker-compose up --build
   ```

   Эта команда создаст и запустит все контейнеры, описанные в `docker-compose.yaml`.

---

### 🔎 Проверка работоспособности сервисов

| Сервис      | Проверка                                            |
| ----------- | --------------------------------------------------- |
| Django      | [http://localhost:8000](http://localhost:8000)      |
| PostgreSQL  | `docker-compose exec db psql -U $POSTGRES_USER`     |
| Redis       | `docker-compose exec redis redis-cli ping` → `PONG` |
| Celery      | `docker-compose logs -f celery`                     |
| Celery Beat | `docker-compose logs -f celery_beat`                |

---

### 🧠 Celery и Celery Beat

Celery запускается через модуль `config`, который содержит точку входа `celery.py`.

Файл `config/celery.py` должен выглядеть так:

```python
from celery import Celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
```

В `config/__init__.py` обязательно подключается приложение Celery:

```python
from .celery import app as celery_app
__all__ = ("celery_app",)
```

Команды запуска в `docker-compose.yaml`:

```yaml
celery:
  command: celery -A config worker --loglevel=info

celery_beat:
  command: celery -A config beat --loglevel=info
```

---

### ⏹️ Остановка проекта

```bash
docker-compose down
```

Чтобы также удалить tom'ы (например, с базой данных):

```bash
docker-compose down -v
```

---

## 🚀 Деплой на удалённый сервер через GitHub Actions

### 📌 Подготовка удалённого сервера

Перед деплоем необходимо:

1. Создать виртуальную машину (например, в Yandex Cloud).
2. Установить на сервер:
   - Docker
   - Docker Compose
3. Настроить SSH-доступ через SSH-ключ.
4. Открыть порты:
   - `22` (SSH)
   - `80` (HTTP)
5. Не нужно вручную клонировать репозиторий — это сделает GitHub Actions.

---

### 🔐 Секреты GitHub

Перейди в:  
**Settings → Secrets and variables → Actions → New repository secret**

Добавь следующие секреты:

| Название                    | Значение                                         |
|-----------------------------|--------------------------------------------------|
| `SSH_USER`                  | логин пользователя на сервере (например, `ubuntu`) |
| `SERVER_IP`                 | публичный IP-адрес сервера                      |
| `SSH_KEY`                   | приватный SSH-ключ (в одном блоке, без пароля)  |
| `DOCKER_HUB_USERNAME`       | имя пользователя Docker Hub                     |
| `DOCKER_HUB_ACCESS_TOKEN`   | access token с правами push/pull                |
| `DOTENV`                    | содержимое `.env` файла, одной строкой          |

---

### ⚙️ Как работает workflow

GitHub Actions запускается при каждом `push` или `pull_request` и выполняет:

1. Проверку стиля кода с помощью `flake8`
2. Запуск тестов (`python manage.py test`)
3. Сборку Docker-образа и загрузку его в Docker Hub
4. Подключение по SSH и перезапуск контейнера на удалённой машине

---

### 🐳 Команды, выполняемые на сервере

```bash
sudo docker pull <ваш-образ>
sudo docker stop myapp || true
sudo docker rm myapp || true
sudo docker run -d --name myapp -p 80:8000 <ваш-образ>
```

### Открыть сайт в браузере
Просто введите в адресной строке:

http://<SERVET_ID> - 158.160.187.166
