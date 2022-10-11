from lib2to3.pgen2 import token
from wsgiref import headers
import pytest
from rest_framework.test import APIClient


@pytest.fixture
def user():
    pass


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()


@pytest.fixture(scope="session")
def registered_api_client(api_client): # ORM
    # Register new user
    token = api_client.post('api/register', payload)
    yield APIClient(headers={"Authorization": f"Bearer {token}"})
    
    # Delete user
