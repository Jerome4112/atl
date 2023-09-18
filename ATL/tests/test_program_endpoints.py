from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from pytest import fixture

from ATL.database import Base
from ATL.main import app
from ATL.dependencies import get_db
from ATL.tests.prep import create_access_token_for_test, create_program_for_test, client

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


def test_create_program():
    access_token = create_access_token_for_test()
    response = create_program_for_test(access_token)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test"
    assert data["licenseKey"] == "ABCDEF-123456-ABCDEF-123456-ABCDEF"
    assert data["version"] == "1.123"
    assert data["installLink"] == "https://www.test.ch"

def test_read_program():
    access_token = create_access_token_for_test()
    create_program_for_test(access_token)
    response = client.get("/program/1", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test"
    assert data["licenseKey"] == "ABCDEF-123456-ABCDEF-123456-ABCDEF"
    assert data["version"] == "1.123"
    assert data["installLink"] == "https://www.test.ch"

def test_update_program():
    access_token = create_access_token_for_test()
    create_program_for_test(access_token)
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    }
    program_data = {
        "id": 1,
        "title": "Test2",
        "licenseKey": "ABCDEF-123456-ABCDEF-123456-ABCDEF",
        "version": "1.123",
        "installLink": "https://www.test.ch",
    }
    response = client.put("/program/1", headers=headers, json=program_data)
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Test2"

def test_delete_program():
    access_token = create_access_token_for_test()
    create_program_for_test(access_token)
    response = client.delete("/program/1", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Test"
    assert data["licenseKey"] == "ABCDEF-123456-ABCDEF-123456-ABCDEF"
    assert data["version"] == "1.123"
    assert data["installLink"] == "https://www.test.ch"


def test_get_program_not_authorised():
    response = client.get("/program/1")
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Not authenticated"

