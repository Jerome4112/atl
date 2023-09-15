import json
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from ATL.database import Base
from ATL.dependencies import get_db
from ATL.main import app

# Erstellen einer SQLite-Datenbank im Speicher für Tests
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Erstellen eines Testclients für die FastAPI-Anwendung
client = TestClient(app)

# Testfunktionen

def test_create_employee():
    employee_data = {
        "first_name": "John",
        "last_name": "Doe",
        "id":"1",
        "email": "johndoe@example.com",
        "tel": "1234567890"
    }
    response = client.post("/employee/1", json=employee_data)
    assert response.status_code == 200
    employee = response.json()
    assert employee["first_name"] == "John"
    assert employee["last_name"] == "Doe"
    #assert employee ["id"] == "1"
    #assert employee["tel"] == "1234567890"

def test_read_employee():
    response = client.get("/employee/1")
    assert response.status_code == 200
    employee = response.json()
    assert employee["first_name"] == "John"
    assert employee["last_name"] == "Doe"
    assert employee["email"] == "johndoe@example.com"
    assert employee["tel"] == "1234567890"
    assert employee["id"] == 1


def test_read_employees():
    response = client.get("/employee/")
    assert response.status_code == 200
    employees = response.json()
    assert len(employees) > 0

def test_update_employee():
    update_data = {
        "first_name": "Updated",
        "last_name": "Employee",
        "id":"1",
        "email": "j.doe@example.com",
        "tel": "987654321"
    }
    response = client.put("/employee/1", json=update_data)
    assert response.status_code == 200
    updated_employee = response.json()
    assert updated_employee["first_name"] == "Updated"
    assert updated_employee["last_name"] == "Employee"
    assert updated_employee["email"] == "j.doe@example.com"
    #assert updated_employee["tel"] == "987654321"
    

def test_delete_employee():
    response = client.delete("/employee/1")
    assert response.status_code == 200
    deleted_employee = response.json()
    assert deleted_employee["first_name"] == "Updated"
    assert deleted_employee["last_name"] == "Employee"

"""def test_read_order_by_employee():
    response = client.get("/employee/1")
    assert response.status_code == 200
    employee_order = response.json()
    # Stellen Sie sicher, dass die employee_order-Daten korrekt sind
"""
# Führen Sie die Tests aus
if __name__ == "__main__":
    import pytest
    pytest.main()
