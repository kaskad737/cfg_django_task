import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from bond_service_api.models import Portfolio, Bond
from django.urls import reverse
from requests import Response


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user1(db):
    return User.objects.create_user(username='user1', password='password1')


@pytest.fixture
def user2(db):
    return User.objects.create_user(username='user2', password='password2')


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(username='admin', email='admin@example.com', password='adminpassword')


@pytest.fixture
def portfolio1(db, user1):
    portfolio = Portfolio.objects.create(name='portfolio1', created_by=user1)
    Bond.objects.create(
        emission_name='bond1_1',
        emission_isin="CZ0003551251",
        bond_value="100",
        interest_rate="15",
        purchase_date="2024-07-06",
        maturity_date="2024-08-06",
        yields_frequency="12",
        portfolio=portfolio
    )
    Bond.objects.create(
        emission_name='bond2_1',
        emission_isin="CZ0008040318",
        bond_value="100",
        interest_rate="15",
        purchase_date="2024-07-06",
        maturity_date="2024-08-06",
        yields_frequency="12",
        portfolio=portfolio
    )
    return portfolio


@pytest.fixture
def portfolio2(db, user2):
    portfolio = Portfolio.objects.create(name='portfolio2', created_by=user2)
    Bond.objects.create(
        emission_name='bond1_2',
        emission_isin="CZ0008040300",
        bond_value="100",
        interest_rate="15",
        purchase_date="2024-07-06",
        maturity_date="2024-08-06",
        yields_frequency="12",
        portfolio=portfolio
    )
    Bond.objects.create(
        emission_name='bond2_2',
        emission_isin="CZ0003532558",
        bond_value="100",
        interest_rate="15",
        purchase_date="2024-07-06",
        maturity_date="2024-08-06",
        yields_frequency="12",
        portfolio=portfolio
    )
    return portfolio


@pytest.fixture
def obtain_access_token(client: APIClient):
    def _obtain_access_token(username, password):
        login_url = reverse('bond_service_api:token_obtain_pair')
        response: Response = client.post(login_url, {
            'username': username,
            'password': password
        })
        return response.data['access']
    return _obtain_access_token


@pytest.fixture
def obtain_refresh_token(api_client: APIClient):
    def _obtain_refresh_token(username, password):
        login_url = reverse('bond_service_api:token_obtain_pair')
        response: Response = api_client.post(login_url, {
            'username': username,
            'password': password
        })
        return response.data['refresh']
    return _obtain_refresh_token


@pytest.fixture
def authenticate_user(api_client: APIClient, obtain_access_token):
    def _authenticate_user(username, password):
        token = obtain_access_token(username=username, password=password)
        api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        return
    return _authenticate_user
