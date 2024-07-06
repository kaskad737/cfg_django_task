import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from bond_service.bond_service_api.models import Portfolio, Bond


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
def portfolio1(db):
    portfolio = Portfolio.objects.create(name='portfolio1')
    Bond.objects.create(emission_name='bond1_1', portfolio=portfolio)
    Bond.objects.create(emission_name='bond2_1', portfolio=portfolio)
    return portfolio


def portfolio2(db):
    portfolio = Portfolio.objects.create(name='portfolio2')
    Bond.objects.create(emission_name='bond1_2', portfolio=portfolio)
    Bond.objects.create(emission_name='bond2_2', portfolio=portfolio)
    return portfolio
