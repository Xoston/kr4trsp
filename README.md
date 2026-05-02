## Установка

    python -m venv .venv
    source .venv/bin/activate
    .venv\Scripts\activate
    pip install -r requirements.txt

## Миграции

    alembic upgrade head
    python seed.py
    alembic upgrade head

## Запуск

    python run.py

## Тестирование

    pytest -v
