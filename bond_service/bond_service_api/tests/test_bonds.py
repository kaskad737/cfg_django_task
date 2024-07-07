import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from requests import Response
from django.db.models.query import QuerySet
from ..models import Portfolio, Bond


@pytest.mark.django_db
def test_user_sees_his_bonds(
    api_client: APIClient,
    authenticate_user,
    user1: User,
    portfolio1: Portfolio
):
    list_bonds_url = reverse('bond_service_api:bond')
    authenticate_user(username='user1', password='password1')
    response: Response = api_client.get(list_bonds_url)
    all_bonds: QuerySet[Bond] = portfolio1.bonds.all()
    for index, bond in enumerate(all_bonds):
        assert response.data['results'][index]['emission_name'] == bond.emission_name
        assert response.data['results'][index]['emission_isin'] == bond.emission_isin
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_dont_see_others_bonds(
    api_client: APIClient,
    authenticate_user,
    user1: User,
    portfolio1: Portfolio,
    portfolio2: Portfolio
):
    list_bonds_url = reverse('bond_service_api:bond')
    authenticate_user(username='user1', password='password1')
    response: Response = api_client.get(list_bonds_url)
    all_bonds: QuerySet[Bond] = portfolio2.bonds.all()
    for index, bond in enumerate(all_bonds):
        assert response.data['results'][index]['emission_name'] != bond.emission_name
        assert response.data['results'][index]['emission_isin'] != bond.emission_isin
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_can_create_bond(
    api_client: APIClient,
    authenticate_user,
    user1: User,
    portfolio1: Portfolio
):
    list_bonds_url = reverse('bond_service_api:bond')
    authenticate_user(username='user1', password='password1')
    data = {
        'emission_name': 'test_emision_name3',
        'emission_isin': 'CZ0009013306',
        'bond_value': '105',
        'interest_rate': '15.00',
        'purchase_date': '2024-07-06',
        'maturity_date': '2024-08-06',
        'yields_frequency': 12,
        'portfolio': portfolio1.pk
    }
    response: Response = api_client.post(list_bonds_url, data=data)
    assert response.data['emission_name'] == data['emission_name']
    assert response.data['emission_isin'] == data['emission_isin']
    assert response.data['interest_rate'] == data['interest_rate']
    assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_user_cant_create_bond_not_in_his_portfolio(
    api_client: APIClient,
    authenticate_user,
    user1: User,
    portfolio2: Portfolio
):
    list_bonds_url = reverse('bond_service_api:bond')
    authenticate_user(username='user1', password='password1')
    data = {
        'emission_name': 'test_emision_name3',
        'emission_isin': 'CZ0009013306',
        'bond_value': '105',
        'interest_rate': '15.00',
        'purchase_date': '2024-07-06',
        'maturity_date': '2024-08-06',
        'yields_frequency': 12,
        'portfolio': portfolio2.pk
    }
    response: Response = api_client.post(list_bonds_url, data=data)
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_user_cant_create_bond_in_his_portfolio_with_bad_emission_isin(
    api_client: APIClient,
    authenticate_user,
    user1: User,
    portfolio1: Portfolio
):
    list_bonds_url = reverse('bond_service_api:bond')
    authenticate_user(username='user1', password='password1')
    data = {
        'emission_name': 'test_emision_name4',
        'emission_isin': 'CZ0001004115',
        'bond_value': '105',
        'interest_rate': '15.00',
        'purchase_date': '2024-07-06',
        'maturity_date': '2024-08-06',
        'yields_frequency': 12,
        'portfolio': portfolio1.pk
    }
    response: Response = api_client.post(list_bonds_url, data=data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_user_can_get_his_bond(
        api_client: APIClient,
        authenticate_user,
        user1: User,
        portfolio1: Portfolio
):
    first_bond: Bond = portfolio1.bonds.all().first()
    bond_url = reverse('bond_service_api:bond_details', kwargs={'pk': first_bond.pk})
    authenticate_user(username='user1', password='password1')
    response: Response = api_client.get(bond_url)
    assert response.data['emission_name'] == first_bond.emission_name
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_cant_see_other_bond(
        api_client: APIClient,
        authenticate_user,
        user1: User,
        portfolio2: Portfolio
):
    first_bond: Bond = portfolio2.bonds.all().first()
    bond_url = reverse('bond_service_api:bond_details', kwargs={'pk': first_bond.pk})
    authenticate_user(username='user1', password='password1')
    response: Response = api_client.get(bond_url)
    assert 'detail' not in response or response['detail'] is None
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_user_can_put_bond(
    api_client: APIClient,
    authenticate_user,
    user1: User,
    portfolio1: Portfolio
):
    first_bond: Bond = portfolio1.bonds.all().first()
    bond_url = reverse('bond_service_api:bond_details', kwargs={'pk': first_bond.pk})
    authenticate_user(username='user1', password='password1')
    old_bond_emission_name = first_bond.emission_name
    new_bond_emission_name = 'new_bond_emission_name'
    data = {
        'emission_name': new_bond_emission_name,
        'emission_isin': 'CZ0003551251',
        'bond_value': '105',
        'interest_rate': '15.00',
        'purchase_date': '2024-07-06',
        'maturity_date': '2024-08-06',
        'yields_frequency': 12,
        'portfolio': portfolio1.pk
    }
    response: Response = api_client.put(bond_url, data=data)
    assert response.data['emission_name'] != old_bond_emission_name
    assert response.data['emission_name'] == new_bond_emission_name
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_cant_put_bond(
    api_client: APIClient,
    authenticate_user,
    user1: User,
    portfolio2: Portfolio
):
    first_bond: Bond = portfolio2.bonds.all().first()
    bond_url = reverse('bond_service_api:bond_details', kwargs={'pk': first_bond.pk})
    authenticate_user(username='user1', password='password1')
    new_bond_emission_name = 'new_bond_emission_name'
    data = {
        'emission_name': new_bond_emission_name,
        'emission_isin': 'CZ0003551251',
        'bond_value': '105',
        'interest_rate': '15.00',
        'purchase_date': '2024-07-06',
        'maturity_date': '2024-08-06',
        'yields_frequency': 12,
        'portfolio': portfolio2.pk
    }
    response: Response = api_client.put(bond_url, data=data)
    assert 'detail' not in response or response['detail'] is None
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_user_can_patch_bond(
    api_client: APIClient,
    authenticate_user,
    user1: User,
    portfolio1: Portfolio
):
    first_bond: Bond = portfolio1.bonds.all().first()
    bond_url = reverse('bond_service_api:bond_details', kwargs={'pk': first_bond.pk})
    authenticate_user(username='user1', password='password1')
    old_bond_emission_name = first_bond.emission_name
    new_bond_emission_name = 'new_bond_emission_name'
    data = {
        'emission_name': new_bond_emission_name
    }
    response: Response = api_client.patch(bond_url, data=data)
    assert response.data['emission_name'] != old_bond_emission_name
    assert response.data['emission_name'] == new_bond_emission_name
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_cant_patch_bond(
    api_client: APIClient,
    authenticate_user,
    user1: User,
    portfolio2: Portfolio
):
    first_bond: Bond = portfolio2.bonds.all().first()
    bond_url = reverse('bond_service_api:bond_details', kwargs={'pk': first_bond.pk})
    authenticate_user(username='user1', password='password1')
    new_bond_emission_name = 'new_bond_emission_name'
    data = {
        'emission_name': new_bond_emission_name
    }
    response: Response = api_client.patch(bond_url, data=data)
    assert 'detail' not in response or response['detail'] is None
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_user_can_delete_bond(
    api_client: APIClient,
    authenticate_user,
    user1: User,
    portfolio1: Portfolio
):
    first_bond: Bond = portfolio1.bonds.all().first()
    bond_url = reverse('bond_service_api:bond_details', kwargs={'pk': first_bond.pk})
    authenticate_user(username='user1', password='password1')
    response: Response = api_client.delete(bond_url)
    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_user_cant_delete_bond(
    api_client: APIClient,
    authenticate_user,
    user1: User,
    portfolio2: Portfolio
):
    first_bond: Bond = portfolio2.bonds.all().first()
    bond_url = reverse('bond_service_api:bond_details', kwargs={'pk': first_bond.pk})
    authenticate_user(username='user1', password='password1')
    response: Response = api_client.delete(bond_url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
