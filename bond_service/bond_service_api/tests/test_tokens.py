import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from requests import Response


@pytest.mark.django_db
def test_authentication(api_client: APIClient, user1: User):
    login_url = reverse('bond_service_api:token_obtain_pair')
    response: Response = api_client.post(login_url, {
        'username': 'user1',
        'password': 'password1'
    })
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_bad_authentication(api_client: APIClient, user1: User):
    login_url = reverse('bond_service_api:token_obtain_pair')
    response: Response = api_client.post(login_url, {
        'username': 'user1',
        'password': 'bad_password'
    })
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_token_refresh(api_client: APIClient, obtain_refresh_token, user1):
    refresh_url = reverse('bond_service_api:token_refresh')
    refresh_token = obtain_refresh_token(username='user1', password='password1')
    response: Response = api_client.post(refresh_url, {
        'refresh': refresh_token
    })
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_token_verify(api_client: APIClient, obtain_access_token, user1):
    verify_url = reverse('bond_service_api:token_verify')
    access_token = obtain_access_token(username='user1', password='password1')
    response: Response = api_client.post(verify_url, {
        'token': access_token
    })
    assert response.status_code == status.HTTP_200_OK
