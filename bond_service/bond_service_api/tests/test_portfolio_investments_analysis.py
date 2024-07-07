import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from requests import Response
from ..models import Portfolio, Bond
from decimal import Decimal
from django.db.models.query import QuerySet


@pytest.mark.django_db
def test_user_get_his_portfolio_analysis(
    api_client: APIClient,
    authenticate_user,
    user1: User,
    portfolio1: Portfolio
):
    all_portfolio_bonds: QuerySet[Bond] = portfolio1.bonds.all()
    nearest_maturity_bond: Bond = min(all_portfolio_bonds, key=lambda bond: bond.maturity_date)
    list_portfolios_url = reverse('bond_service_api:portfolio_investment_analysis')
    authenticate_user(username='user1', password='password1')
    response: Response = api_client.get(list_portfolios_url, data={'portfolio_pk': portfolio1.pk})
    assert response.data['average_interest_rate'] == Decimal('15.00')
    assert response.data['nearest_maturity_bond']['emission_name'] == nearest_maturity_bond.emission_name
    assert response.data['total_value'] == Decimal('200.00')
    assert response.data['future_value'] == Decimal('202.3091123419387225004762924')
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_user_cant_get_others_portfolio_analysis(
    api_client: APIClient,
    authenticate_user,
    user1: User,
    portfolio2: Portfolio
):
    list_portfolios_url = reverse('bond_service_api:portfolio_investment_analysis')
    authenticate_user(username='user1', password='password1')
    response: Response = api_client.get(list_portfolios_url, data={'portfolio_pk': portfolio2.pk})
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_admin_get_portfolio_analysis(
    api_client: APIClient,
    authenticate_user,
    admin_user: User,
    portfolio1: Portfolio
):
    all_portfolio_bonds: QuerySet[Bond] = portfolio1.bonds.all()
    nearest_maturity_bond: Bond = min(all_portfolio_bonds, key=lambda bond: bond.maturity_date)
    list_portfolios_url = reverse('bond_service_api:portfolio_investment_analysis')
    authenticate_user(username='admin', password='adminpassword')
    response: Response = api_client.get(list_portfolios_url, data={'portfolio_pk': portfolio1.pk})
    assert response.data['average_interest_rate'] == Decimal('15.00')
    assert response.data['nearest_maturity_bond']['emission_name'] == nearest_maturity_bond.emission_name
    assert response.data['total_value'] == Decimal('200.00')
    assert response.data['future_value'] == Decimal('202.3091123419387225004762924')
    assert response.status_code == status.HTTP_200_OK
