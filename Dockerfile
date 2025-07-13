FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libpq-dev \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get clean

WORKDIR /app

RUN pip install poetry==2.1.3

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && \
    poetry install --no-root --only main  && \
    poetry add gunicorn

COPY . .

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
