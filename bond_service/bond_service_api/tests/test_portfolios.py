import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from requests import Response
from ..models import Portfolio


@pytest.mark.django_db
def test_user_sees_his_portfolios(
    api_client: APIClient,
    authenticate_user,
    user1: User,
    portfolio1: Portfolio
):
    list_portfolios_url = reverse('bond_service_api:portfolio')
    authenticate_user(username='user1', password='password1')
    response: Response = api_client.get(list_portfolios_url)
    assert response.data['results'][0]['name'] == portfolio1.name
    assert response.data['results'][0]['created_at'] == portfolio1.created_at.strftime('%Y-%m-%d')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_dont_see_others_portfolios(
    api_client: APIClient,
    authenticate_user,
    user1: User,
    portfolio2: Portfolio
):
    list_portfolios_url = reverse('bond_service_api:portfolio')
    authenticate_user(username='user1', password='password1')
    response: Response = api_client.get(list_portfolios_url)
    assert response.data['results'] == []
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_can_create_portfolio(
    api_client: APIClient,
    authenticate_user,
    user1: User
):
    list_portfolios_url = reverse('bond_service_api:portfolio')
    authenticate_user(username='user1', password='password1')
    new_portfolio_name = 'new_test_portfolio'
    data = {
        'name': new_portfolio_name
    }
    response: Response = api_client.post(list_portfolios_url, data=data)
    assert response.data['name'] == new_portfolio_name
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_user_can_get_his_portfolio(
        api_client: APIClient,
        authenticate_user,
        user1: User,
        portfolio1: Portfolio
):
    portfolio_url = reverse('bond_service_api:portfolio_details', kwargs={'pk': portfolio1.pk})
    authenticate_user(username='user1', password='password1')
    response: Response = api_client.get(portfolio_url)
    assert response.data['name'] == portfolio1.name
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_cant_see_other_portfolio(
        api_client: APIClient,
        authenticate_user,
        user1: User,
        portfolio2: Portfolio
):
    portfolio_url = reverse('bond_service_api:portfolio_details', kwargs={'pk': portfolio2.pk})
    authenticate_user(username='user1', password='password1')
    response: Response = api_client.get(portfolio_url)
    assert 'detail' not in response or response['detail'] is None
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_user_can_put_portfolio(
    api_client: APIClient,
    authenticate_user,
    user1: User,
    portfolio1: Portfolio
):
    portfolio_url = reverse('bond_service_api:portfolio_details', kwargs={'pk': portfolio1.pk})
    authenticate_user(username='user1', password='password1')
    old_portfolio_name = portfolio1.pk
    new_portfolio_name = 'new_test_portfolio'
    data = {
        'name': new_portfolio_name
    }
    response: Response = api_client.put(portfolio_url, data=data)
    assert response.data['name'] != old_portfolio_name
    assert response.data['name'] == new_portfolio_name
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_cant_put_portfolio(
    api_client: APIClient,
    authenticate_user,
    user1: User,
    portfolio2: Portfolio
):
    portfolio_url = reverse('bond_service_api:portfolio_details', kwargs={'pk': portfolio2.pk})
    authenticate_user(username='user1', password='password1')
    new_portfolio_name = 'new_test_portfolio'
    data = {
        'name': new_portfolio_name
    }
    response: Response = api_client.put(portfolio_url, data=data)
    assert 'detail' not in response or response['detail'] is None
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_user_can_patch_portfolio(
    api_client: APIClient,
    authenticate_user,
    user1: User,
    portfolio1: Portfolio
):
    portfolio_url = reverse('bond_service_api:portfolio_details', kwargs={'pk': portfolio1.pk})
    authenticate_user(username='user1', password='password1')
    old_portfolio_name = portfolio1.pk
    new_portfolio_name = 'new_test_portfolio'
    data = {
        'name': new_portfolio_name
    }
    response: Response = api_client.patch(portfolio_url, data=data)
    assert response.data['name'] != old_portfolio_name
    assert response.data['name'] == new_portfolio_name
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_cant_patch_portfolio(
    api_client: APIClient,
    authenticate_user,
    user1: User,
    portfolio2: Portfolio
):
    portfolio_url = reverse('bond_service_api:portfolio_details', kwargs={'pk': portfolio2.pk})
    authenticate_user(username='user1', password='password1')
    new_portfolio_name = 'new_test_portfolio'
    data = {
        'name': new_portfolio_name
    }
    response: Response = api_client.patch(portfolio_url, data=data)
    assert 'detail' not in response or response['detail'] is None
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_user_can_delete_portfolio(
    api_client: APIClient,
    authenticate_user,
    user1: User,
    portfolio1: Portfolio
):
    portfolio_url = reverse('bond_service_api:portfolio_details', kwargs={'pk': portfolio1.pk})
    authenticate_user(username='user1', password='password1')
    response: Response = api_client.delete(portfolio_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_user_cant_delete_portfolio(
    api_client: APIClient,
    authenticate_user,
    user1: User,
    portfolio2: Portfolio
):
    portfolio_url = reverse('bond_service_api:portfolio_details', kwargs={'pk': portfolio2.pk})
    authenticate_user(username='user1', password='password1')
    response: Response = api_client.delete(portfolio_url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
