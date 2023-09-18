from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from pytest import fixture

from ATL.database import Base
from ATL.main import app
from ATL.dependencies import get_db
from ATL.tests.prep import create_access_token_for_test, client

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

def test_user_login():
    create_access_token_for_test()
    response = client.post("/user/login", data={"username": "testuser", "password": "Test"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["access_token"] is not None
    assert data["token_type"] == "bearer"

def test_user_login_wrong_password():
    create_access_token_for_test()
    response = client.post("/user/login", data={"username": "testuser", "password": "wrong"})
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Incorrect username or password"