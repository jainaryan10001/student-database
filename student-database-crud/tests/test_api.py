import importlib
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

import main


@pytest.fixture()
def client(tmp_path, monkeypatch):
    database = tmp_path / "test_students.db"
    monkeypatch.setattr(main, "DATABASE_PATH", database)
    with TestClient(main.app) as test_client:
        yield test_client


def sample_student(email="aarav.demo@example.com"):
    return {
        "name": "Aarav Sharma",
        "date_of_birth": "2005-04-17",
        "email": email,
        "phone": "+91 9876543210",
        "course": "BCA",
        "address": "Demo Address",
        "enrollment_date": "2025-08-01",
    }


def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_create_and_list_student(client):
    created = client.post("/students", json=sample_student())
    assert created.status_code == 201
    assert created.json()["name"] == "Aarav Sharma"
    assert created.json()["student_id"] == 1

    listed = client.get("/students")
    assert listed.status_code == 200
    assert listed.json()["total"] == 1
    assert listed.json()["students"][0]["email"] == "aarav.demo@example.com"


def test_get_missing_student_returns_404(client):
    response = client.get("/students/999")
    assert response.status_code == 404


def test_duplicate_email_returns_409(client):
    assert client.post("/students", json=sample_student()).status_code == 201
    response = client.post("/students", json=sample_student())
    assert response.status_code == 409


def test_update_student(client):
    created = client.post("/students", json=sample_student())
    student_id = created.json()["student_id"]

    response = client.put(f"/students/{student_id}", json={"course": "BCA - AI"})
    assert response.status_code == 200
    assert response.json()["course"] == "BCA - AI"
    assert response.json()["name"] == "Aarav Sharma"


def test_delete_student(client):
    created = client.post("/students", json=sample_student())
    student_id = created.json()["student_id"]

    deleted = client.delete(f"/students/{student_id}")
    assert deleted.status_code == 200
    assert client.get(f"/students/{student_id}").status_code == 404


def test_invalid_email_is_rejected(client):
    response = client.post("/students", json=sample_student("not-an-email"))
    assert response.status_code == 422


def test_filter_by_name(client):
    client.post("/students", json=sample_student())
    client.post("/students", json=sample_student("meera.demo@example.com") | {"name": "Meera Verma"})

    response = client.get("/students?name=Meera")
    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["students"][0]["name"] == "Meera Verma"
