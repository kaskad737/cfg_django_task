import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from requests import Response


@pytest.mark.django_db
def test_registration(api_client: APIClient):
    data = {
        "username": "creation_test_user",
        "password": "creation_test_user",
        "password2": "creation_test_user",
        "email": "test@email.com",
        "first_name": "John",
        "last_name": "Doe"
    }

    url = reverse('bond_service_api:user_register')
    response: Response = api_client.post(url, data=data)

    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_bad_registration(api_client: APIClient):
    data = {
        "username": "",
        "password": "creation_test_user",
        "password2": "creation_test_user",
        "email": "test@email.com",
        "first_name": "John",
        "last_name": "Doe"
    }

    url = reverse('bond_service_api:user_register')
    response: Response = api_client.post(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
