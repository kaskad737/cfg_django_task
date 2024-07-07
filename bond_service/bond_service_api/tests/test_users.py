import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from requests import Response


@pytest.mark.django_db
def test_admin_can_list_users(api_client: APIClient, authenticate_user, admin_user: User):
    list_users_url = reverse('bond_service_api:users')
    authenticate_user(username='admin', password='adminpassword')
    response: Response = api_client.get(list_users_url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_admin_can_get_user(api_client: APIClient, authenticate_user, user1: User, admin_user: User):
    user_url = reverse('bond_service_api:user_details', kwargs={'pk': user1.pk})
    authenticate_user(username='admin', password='adminpassword')
    response: Response = api_client.get(user_url)
    assert response.data['username'] == 'user1'
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_admin_can_put_user(api_client: APIClient, authenticate_user, user1: User, admin_user: User):
    user_url = reverse('bond_service_api:user_details', kwargs={'pk': user1.pk})
    authenticate_user(username='admin', password='adminpassword')
    data = {
        'username': 'newusername',
        'email': 'newemail@example.com',
        'password': 'newpassword123'
    }
    response: Response = api_client.put(user_url, data=data)
    assert response.data['username'] == 'newusername'
    assert response.data['email'] == 'newemail@example.com'
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_admin_can_patch_user(api_client: APIClient, authenticate_user, user1: User, admin_user: User):
    user_url = reverse('bond_service_api:user_details', kwargs={'pk': user1.pk})
    authenticate_user(username='admin', password='adminpassword')
    data = {
        'username': 'newusername'
    }
    response: Response = api_client.patch(user_url, data=data)
    assert response.data['username'] == 'newusername'
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_admin_can_delete_user(api_client: APIClient, authenticate_user, user1: User, admin_user: User):
    user_url = reverse('bond_service_api:user_details', kwargs={'pk': user1.pk})
    authenticate_user(username='admin', password='adminpassword')
    response: Response = api_client.delete(user_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_user_cant_list_users(api_client: APIClient, authenticate_user, user1: User):
    list_users_url = reverse('bond_service_api:users')
    authenticate_user(username='user1', password='password1')
    response: Response = api_client.get(list_users_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_cant_get_user(api_client: APIClient, authenticate_user, user1: User, user2: User):
    user_url = reverse('bond_service_api:user_details', kwargs={'pk': user2.pk})
    authenticate_user(username='user1', password='password1')
    response: Response = api_client.get(user_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_cant_put_user(api_client: APIClient, authenticate_user, user1: User, user2: User):
    user_url = reverse('bond_service_api:user_details', kwargs={'pk': user2.pk})
    authenticate_user(username='user1', password='password1')
    data = {
        'username': 'newusername',
        'email': 'newemail@example.com',
        'password': 'newpassword123'
    }
    response: Response = api_client.put(user_url, data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_cant_patch_user(api_client: APIClient, authenticate_user, user1: User, user2: User):
    user_url = reverse('bond_service_api:user_details', kwargs={'pk': user2.pk})
    authenticate_user(username='user1', password='password1')
    data = {
        'username': 'newusername'
    }
    response: Response = api_client.patch(user_url, data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_cant_delete_user(api_client: APIClient, authenticate_user, user1: User, user2: User):
    user_url = reverse('bond_service_api:user_details', kwargs={'pk': user2.pk})
    authenticate_user(username='user1', password='password1')
    response: Response = api_client.delete(user_url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
