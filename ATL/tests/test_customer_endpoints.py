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
    # Erstellen Sie die Daten für Ihren Testbenutzer
    test_user_data = {
        "name": "testuser",
        "hashed_password": "hashed_password_here",  # Sie sollten das echte gehashte Passwort hier einfügen
        "is_authorised": True  # Oder False, je nachdem, ob der Benutzer authorisiert sein soll oder nicht
    }

    # Senden Sie eine POST-Anfrage, um den Testbenutzer zu registrieren
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


        
def test_create_customer():
    access_token = create_access_token_for_test()
    response = create_customer_for_test(access_token)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Customer"
    assert data["adress"] == "Test Adress"
    assert data["adressNr"] == 1
    assert data["email"] == "test@test.ch"
    assert data["tel"] == 123456789
    assert data["city"] == "Test City"
    assert data["postalCode"] == 1234
    assert data["id"] == 1

def test_read_customer():
    access_token = create_access_token_for_test()
    create_customer_for_test(access_token)
    response = client.get("/customer/1", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Customer"
    assert data["id"] == 1

def test_read_customer_not_found():
    access_token = create_access_token_for_test()
    create_customer_for_test(access_token)
    response = client.get("/customer/2", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Customer not found"

def test_read_all_customer():
    access_token = create_access_token_for_test()
    create_customer_for_test(access_token)
    client.post(
        "/customer/",headers={"Authorization": f"Bearer {access_token}"},
        json={
            "id": 2,    
            "name": "Test Customer 2",
            "adress": "Test Adress",
             "adressNr": 2,
            "email": "test2@test2.ch",
            "tel": 123456789,
            "city": "Test City2",
            "postalCode": 123456,
            },
        )
    response = client.get("/customer/", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Test Customer"
    assert data[1]["name"] == "Test Customer 2"
    assert data[0]["id"] == 1
    assert data[1]["id"] == 2


def test_update_customer():
    access_token = create_access_token_for_test()
    create_customer_for_test(access_token)
    response = client.put(
        "/customer/1", headers={"Authorization": f"Bearer {access_token}"},
        json={
            "id": 1,
            "name": "Test Customer 2",
            "adress": "Test Adress 2",
            "adressNr": 2,
            "email": "test@test2.ch",
            "tel": 123456789,
            "city": "Test City 2",
            "postalCode": 123456,
        },
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Customer 2"
    assert data["adress"] == "Test Adress 2"
    assert data["adressNr"] == 2
    assert data["email"] == "test@test2.ch"
    assert data["tel"] == 123456789
    assert data["city"] == "Test City 2"
    assert data["postalCode"] == 123456
    assert data["id"] == 1

def test_delete_customer():
    access_token = create_access_token_for_test()
    create_customer_for_test(access_token)
    response = client.delete("/customer/1", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200, response.text
    


