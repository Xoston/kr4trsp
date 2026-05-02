import pytest

@pytest.mark.asyncio
async def test_validation_error(async_client):
    invalid = {"username": "a", "age": 15, "email": "x", "password": "123"}
    resp = await async_client.post("/users/", json=invalid)
    assert resp.status_code == 422
    data = resp.json()
    assert data["message"] == "Validation error"
    assert len(data["errors"]) > 0

@pytest.mark.asyncio
async def test_custom_exception_a(async_client, faker):
    data = {
        "username": faker.user_name(),
        "age": 17,
        "email": faker.email(),
        "password": faker.password(length=10),
        "phone": faker.phone_number()
    }
    resp = await async_client.post("/users/", json=data)
    assert resp.status_code == 400
    assert resp.json()["error_type"] == "CustomExceptionA"

@pytest.mark.asyncio
async def test_custom_exception_b(async_client):
    resp = await async_client.get("/products/99999")
    assert resp.status_code == 404
    assert resp.json()["error_type"] == "CustomExceptionB"