from pytest import fixture
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from app.main import app
from app.models import Post, User
from app.config import settings as s
from app.database import get_db, Base
from app.oauth2 import create_access_token

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


@fixture
def test_user2(client):
    user_data = {"email": "abc1@d.e", "password": "123"}
    res = client.post("/users", json=user_data)

    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = "123"
    return new_user


@fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})


@fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "Authorization": f"Bearer {token}"}
    return client


@fixture
def test_posts(test_user, test_user2, session):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "user_id": test_user["id"],
        },
        {"title": "2nd title", "content": "2nd content", "user_id": test_user["id"]},
        {"title": "3rd title", "content": "3rd content", "user_id": test_user["id"]},
        {"title": "3rd title", "content": "3rd content", "user_id": test_user2["id"]},
    ]

    posts = list(map(lambda post: Post(**post), posts_data))
    session.add_all(posts)

    session.commit()
    posts = session.query(Post).all()
    return posts
