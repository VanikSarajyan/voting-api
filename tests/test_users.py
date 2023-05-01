from pytest import mark
from app.schemas import UserResponseSchema, TokenSchema


def test_root(client):
    res = client.get("/")
    assert res.json().get("welcome") == "voting-api"
    assert res.status_code == 200


def test_create_user(client):
    res = client.post("/users", json={"email": "abcd@gmail.com", "password": "123"})
    new_user = UserResponseSchema(**res.json())
    assert new_user.email == "abcd@gmail.com"
    assert res.status_code == 201


def test_login(client, test_user):
    res = client.post(
        "/login",
        data={"username": test_user["email"], "password": test_user["password"]},
    )
    token = TokenSchema(**res.json())
    assert res.status_code == 200


@mark.parametrize(
    "email, password, status_code",
    [("wrong@mail.am", "123", 403), (None, "123", 422), ("abc@d.e", None, 422)],
)
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post(
        "/login",
        data={"username": email, "password": password},
    )
    assert res.status_code == status_code
