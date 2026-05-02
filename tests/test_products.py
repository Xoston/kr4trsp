import pytest

@pytest.mark.asyncio
async def test_create_product(async_client, faker):
    product_data = {
        "title": faker.word(),
        "price": 99.99,
        "count": 10,
        "description": faker.sentence()
    }
    resp = await async_client.post("/products/", json=product_data)
    assert resp.status_code == 201
    data = resp.json()
    assert data["description"] == product_data["description"]

@pytest.mark.asyncio
async def test_get_product_not_found(async_client):
    resp = await async_client.get("/products/777")
    assert resp.status_code == 404