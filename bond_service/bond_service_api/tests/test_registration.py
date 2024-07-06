import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User


@pytest.mark.django_db
def obtain_token(api_client: APIClient, username, password):
    login_url = reverse('bond_service_api:token_obtain_pair')
    response = api_client.post(login_url, {
        'username': username,
        'password': password
    })
    assert response.status_code == status.HTTP_200_OK
    return response.data['access']


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
    response = api_client.post(url, data=data)

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
    response = api_client.post(url, data=data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_authentication(api_client: APIClient, user1: User):
    login_url = reverse('bond_service_api:token_obtain_pair')
    response = api_client.post(login_url, {
        'username': 'user1',
        'password': 'password1'
    })
    assert response.status_code == status.HTTP_200_OK
