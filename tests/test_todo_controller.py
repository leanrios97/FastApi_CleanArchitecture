import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_create_todo():
    response = client.post("/todos", json={"title": "Test Todo", "description": "Test Description"})
    assert response.status_code == 200
    assert response.json()["title"] == "Test Todo"

def test_get_todo():
    response = client.post("/todos", json={"title": "Test Todo", "description": "Test Description"})
    todo_id = response.json()["id"]
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Test Todo"

def test_list_todos():
    response = client.get("/todos")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_todo():
    response = client.post("/todos", json={"title": "Test Todo", "description": "Test Description"})
    todo_id = response.json()["id"]
    response = client.put("/todos", json={
        "id": todo_id,
        "title": "Updated Todo",
        "description": "Updated Description",
        "completed": True
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Todo"
    assert response.json()["completed"] is True

def test_delete_todo():
    response = client.post("/todos", json={"title": "Test Todo", "description": "Test Description"})
    todo_id = response.json()["id"]
    response = client.delete(f"/todos/{todo_id}")
    assert response.status_code == 204
    response = client.get(f"/todos/{todo_id}")
    assert response.status_code == 404

def test_delete_todo_not_found():
    response = client.delete("/todos/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Todo not found"