from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from pytest import fixture

from ATL.database import Base
from ATL.main import app
from ATL.dependencies import get_db
from ATL.tests.prep import create_access_token_for_test, create_customer_for_test, create_employee_for_test,create_order_for_test, client #Testdaten importieren

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

@fixture(scope="function", autouse=True)
def clear_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_create_order():
    access_token = create_access_token_for_test()
    create_customer_for_test(access_token)
    create_employee_for_test(access_token)
    response = create_order_for_test(access_token)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test"
    assert data["hardware"] == "Test"
    assert data["details"] == "Test"

def test_read_order():
    access_token = create_access_token_for_test()
    create_customer_for_test(access_token)
    create_employee_for_test(access_token)
    create_order_for_test(access_token)
    response = client.get("/order/1", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test"
    assert data["hardware"] == "Test"
    assert data["details"] == "Test"
    assert data["programs"] == []

def test_update_order():
    access_token = create_access_token_for_test()
    create_customer_for_test(access_token)
    create_employee_for_test(access_token)
    create_order_for_test(access_token)
    response = client.put("/order/1", headers={"Authorization": f"Bearer {access_token}"}, json={"id": 1,"title": "Test2", "hardware": "Test2", "details": "Test2"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test2"
    assert data["hardware"] == "Test2"
    assert data["details"] == "Test2"

def test_delete_order():
    access_token = create_access_token_for_test()
    create_customer_for_test(access_token)
    create_employee_for_test(access_token)
    create_order_for_test(access_token)
    response = client.delete("/order/1", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test"
    assert data["hardware"] == "Test"
    assert data["details"] == "Test"

def test_get_order_not_authorised():
    response = client.get("/order/1")
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Not authenticated"
