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

def create_order_for_test(access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    order_data = {
        "id": 1,
        "title": "Test Order",
        "hardware": "Test Hardware",
        "details": "Test Details",
    }
    response = client.post(f"/order/{1},{1}", headers=headers, json=order_data)
    return response
