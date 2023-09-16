from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from pytest import fixture

from ATL.database import Base
from ATL.main import app
from ATL.dependencies import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app_test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@fixture(scope="function", autouse=True)
def clear_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

def create_access_token_for_test():
    # Erstellen der Daten für den Testbenutzer
    test_user_data = {
        "name": "testuser",
        "hashed_password": "Test",
        "is_authorised": True  
    }
    # POST-Anfrage, um den Testbenutzer zu registrieren
    response = client.post("/user/register", json=test_user_data)
    # Das Zugriffstoken des Testbenutzers
    access_token = response.json()["access_token"]
    return access_token

def create_customer_for_test(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    customer_data = {
        "id": 1,
        "name": "Test Customer",
        "adress": "Test Adress",
        "adressNr": 1,
        "email": "test@test.ch",
        "tel": 123456789,
        "city": "Test City",
        "postalCode": 1234,
    }
    response = client.post("/customer/", headers=headers, json=customer_data)
    return response

def create_employee_for_test(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    employee_data = {
        "id": 1,
        "first_name": "Test",
        "last_name": "Test",
        "email": "test@test.ch",
        "passwordEmail": "Test",
        "tel": 123456789,
    }
    response = client.post(f"/employee/{1}", headers=headers, json=employee_data)
    return response
#######################################################################################
#####################Tests for Employee Endpoints######################################

def test_create_employee():
    access_token = create_access_token_for_test()
    create_customer_for_test(access_token)
    response = create_employee_for_test(access_token)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == 1
    assert data["first_name"] == "Test"
    assert data["last_name"] == "Test"
    assert data["email"] == "test@test.ch"
    assert data["passwordEmail"] == "Test"
    assert data["tel"] == 123456789
    assert data["orders"] == []

def test_read_employee():
    access_token = create_access_token_for_test()
    create_employee_for_test(access_token)
    response = client.get("/employee/1", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == 1
    assert data["first_name"] == "Test"
    assert data["last_name"] == "Test"
    assert data["email"] == "test@test.ch"
    assert data["passwordEmail"] == "Test"
    assert data["tel"] == 123456789
    assert data["orders"] == []

def test_read_employee_not_found():
    access_token = create_access_token_for_test()
    create_employee_for_test(access_token)
    response = client.get("/employee/2", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Employee not found"

def test_read_employees():
    access_token = create_access_token_for_test()
    create_employee_for_test(access_token)
    client.post(f"/employee/{2}",headers={"Authorization": f"Bearer {access_token}"},
        json={
            "id": 2,
            "first_name": "Test2",
            "last_name": "Test2",
            "email": "test@test2.ch",
            "passwordEmail": "Test2",
            "tel": 123456789,
        }
    )
    response = client.get("/employee/", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["id"] == 1
    assert data[0]["first_name"] == "Test"
    assert data[0]["last_name"] == "Test"
    assert data[0]["orders"] == []
    assert data[1]["id"] == 2
    assert data[1]["first_name"] == "Test2"
    assert data[1]["last_name"] == "Test2"
    assert data[1]["orders"] == []

def test_update_employee():
    access_token = create_access_token_for_test()
    create_employee_for_test(access_token)
    employee_update = {
        "id": 1,
        "first_name": "TestUpdate",
        "last_name": "TestUpdate",
        "email": "test@update.ch",
        "passwordEmail": "TestUpdate",
        "tel": 123456789,
    }
    response = client.put("/employee/1", headers={"Authorization": f"Bearer {access_token}"}, json=employee_update)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == 1
    assert data["first_name"] == "TestUpdate"
    assert data["last_name"] == "TestUpdate"
    assert data["email"] == "test@update.ch"
    assert data["passwordEmail"] == "TestUpdate"

def test_delete_employee():
    access_token = create_access_token_for_test()
    create_employee_for_test(access_token)
    response = client.delete("/employee/1", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == 1
    assert data["first_name"] == "Test"
    assert data["last_name"] == "Test"
    

