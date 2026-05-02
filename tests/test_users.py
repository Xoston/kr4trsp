import pytest

@pytest.mark.asyncio
async def test_create_user_success(async_client, valid_user_data):
    response = await async_client.post("/users/", json=valid_user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["username"] == valid_user_data["username"]
    assert "id" in data

@pytest.mark.asyncio
async def test_get_existing_user(async_client, valid_user_data):
    resp = await async_client.post("/users/", json=valid_user_data)
    user_id = resp.json()["id"]
    resp = await async_client.get(f"/users/{user_id}")
    assert resp.status_code == 200

@pytest.mark.asyncio
async def test_get_nonexistent_user(async_client):
    resp = await async_client.get("/users/999")
    assert resp.status_code == 404

@pytest.mark.asyncio
async def test_delete_user(async_client, valid_user_data):
    resp = await async_client.post("/users/", json=valid_user_data)
    user_id = resp.json()["id"]
    resp = await async_client.delete(f"/users/{user_id}")
    assert resp.status_code == 204
    resp = await async_client.delete(f"/users/{user_id}")
    assert resp.status_code == 404