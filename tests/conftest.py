from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.config import settings as s
from app.database import get_db, Base

TEST_DB_URL = f"postgresql://{s.db_username}:{s.db_password}@{s.db_hostname}:{s.db_port}/{s.db_name}_test"
engine = create_engine(TEST_DB_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


@fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)


@fixture
def test_user(client):
    user_data = {"email": "abc@d.e", "password": "123"}
    res = client.post("/users", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = "123"
    return new_user
