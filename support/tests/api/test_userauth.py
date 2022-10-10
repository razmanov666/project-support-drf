import pytest
from rest_framework.test import APIClient


client = APIClient()


@pytest.mark.django_db
def test_register_user():
    payload = dict(
        username="HarryPotter",
        first_name="Harry",
        second_name="Potter",
        email="buklya@hogwarts.com",
        password="timeforsomethig",
        password2="timeforsomethig",
    )

    response = client.post("/api/register/", payload)

    data = response.data
    assert data["first_name"] == payload["first_name"]
    assert data["second_name"] == payload["second_name"]
    assert "password" not in data
    assert data["email"] == payload["email"]
    assert data["username"] == payload["username"]


@pytest.mark.django_db
def test_login_user():
    payload = dict(
        username="HarryPotter",
        first_name="Harry",
        second_name="Potter",
        email="buklya@hogwarts.com",
        password="timeforsomethig",
        password2="timeforsomethig",
    )

    client.post("/api/support-auth/login/", payload)

    response = client.post(
        "/api/support-auth/login/",
        dict(
            username="HarryPotter",
            password="timeforsomethig",
        ),
    )

    assert response.status_code == 200
