import pytest
from httpx import AsyncClient, ASGITransport
from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

fake = Faker()

# --- in-memory SQLite для тестов продуктов ---
TEST_DATABASE_URL = "sqlite:///./test_test.db"  # можно заменить на :memory: но оставим файл для наглядности
engine_test = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

@pytest.fixture(scope="function")
def db_session():
    # Создаём таблицы
    Base.metadata.create_all(bind=engine_test)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Удаляем таблицы после теста
        Base.metadata.drop_all(bind=engine_test)

@pytest.fixture(autouse=True)
def override_get_db(db_session):
    # Подменяем зависимость get_db на тестовую сессию
    def _override():
        yield db_session
    app.dependency_overrides[get_db] = _override
    yield
    app.dependency_overrides.clear()

# --- клиент ---
@pytest.fixture
async def async_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client

# --- данные ---
@pytest.fixture
def faker():
    return fake

@pytest.fixture
def valid_user_data(faker):
    return {
        "username": faker.user_name(),
        "age": faker.random_int(min=19, max=100),
        "email": faker.email(),
        "password": faker.password(length=10),
        "phone": faker.phone_number()
    }

@pytest.fixture
def invalid_user_data(faker):
    return {
        "username": faker.user_name(),
        "age": 15,
        "email": "invalid-email",
        "password": "short",
        "phone": faker.phone_number()
    }

# Очистка in-memory хранилища users
@pytest.fixture(autouse=True)
def clean_user_storage():
    from app.routers.users import db
    db.clear()
    import app.routers.users as users_module
    from itertools import count
    users_module._id_seq = count(start=1)
    yield
    db.clear()