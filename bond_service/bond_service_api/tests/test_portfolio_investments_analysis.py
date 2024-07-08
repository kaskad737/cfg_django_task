import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from requests import Response
from ..models import Portfolio, Bond
from decimal import Decimal
from django.db.models.query import QuerySet
from django.utils import timezone


@pytest.mark.django_db
def test_user_get_his_portfolio_analysis(
    api_client: APIClient,
    authenticate_user,
    user1: User,
    portfolio1: Portfolio
):
    all_portfolio_bonds: QuerySet[Bond] = portfolio1.bonds.all()
    total_value = Decimal(sum(all_portfolio_bonds.values_list('bond_value', flat=True)))
    avg_interest_rate = Decimal(sum(all_portfolio_bonds.values_list(
        'interest_rate', flat=True)) / all_portfolio_bonds.count())
    nearest_maturity_bond: Bond = min(all_portfolio_bonds, key=lambda bond: bond.maturity_date)
    years = Decimal((nearest_maturity_bond.maturity_date - timezone.now().date()).days / Decimal(365.25))
    future_value = total_value * (1 + avg_interest_rate / 100) ** years
    list_portfolios_url = reverse('bond_service_api:portfolio_investment_analysis')
    authenticate_user(username='user1', password='password1')
    response: Response = api_client.get(list_portfolios_url, data={'portfolio_pk': portfolio1.pk})
    assert response.data['average_interest_rate'] == avg_interest_rate
    assert response.data['nearest_maturity_bond']['emission_name'] == nearest_maturity_bond.emission_name
    assert response.data['total_value'] == total_value
    assert response.data['future_value'] == future_value
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
    total_value = Decimal(sum(all_portfolio_bonds.values_list('bond_value', flat=True)))
    avg_interest_rate = Decimal(sum(all_portfolio_bonds.values_list(
        'interest_rate', flat=True)) / all_portfolio_bonds.count())
    nearest_maturity_bond: Bond = min(all_portfolio_bonds, key=lambda bond: bond.maturity_date)
    years = Decimal((nearest_maturity_bond.maturity_date - timezone.now().date()).days / Decimal(365.25))
    future_value = total_value * (1 + avg_interest_rate / 100) ** years
    list_portfolios_url = reverse('bond_service_api:portfolio_investment_analysis')
    authenticate_user(username='admin', password='adminpassword')
    response: Response = api_client.get(list_portfolios_url, data={'portfolio_pk': portfolio1.pk})
    assert response.data['average_interest_rate'] == avg_interest_rate
    assert response.data['nearest_maturity_bond']['emission_name'] == nearest_maturity_bond.emission_name
    assert response.data['total_value'] == total_value
    assert response.data['future_value'] == future_value
    assert response.status_code == status.HTTP_200_OK
