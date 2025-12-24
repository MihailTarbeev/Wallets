import pytest
from django.test import Client
from wallets.models import Wallet, Operation
from decimal import Decimal
import uuid
from django.contrib.auth.models import User


@pytest.fixture
def api_client():
    return Client()


@pytest.fixture(scope="function")
def test_user():
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={'email': 'test@example.com', 'password': 'testpass123'}
    )
    return user


@pytest.fixture
def authenticated_api_client(test_user):
    client = Client()
    client.force_login(test_user)
    return client


@pytest.fixture(scope="function")
def temp_wallet_default(test_user):
    wallet = Wallet.objects.create(user=test_user)
    return wallet


@pytest.fixture(scope="function")
def temp_wallet_1000(test_user):
    wallet = Wallet.objects.create(user=test_user, balance=Decimal('1000.00'))
    return wallet


@pytest.fixture(scope="function")
def temp_operation_dep_100(temp_wallet_1000, test_user):
    operation = Operation.objects.create(
        transaction_id=uuid.uuid4(),
        operation_type='DEPOSIT',
        amount=Decimal('100.00'),
        wallet=temp_wallet_1000,
        user=test_user
    )
    return operation


@pytest.fixture(scope="function")
def temp_operation_wid_500(temp_wallet_1000, test_user):
    operation = Operation.objects.create(
        transaction_id=uuid.uuid4(),
        operation_type='WITHDRAW',
        amount=Decimal('500.00'),
        wallet=temp_wallet_1000,
        user=test_user
    )
    return operation


@pytest.fixture(scope="function")
def withdraw_300():
    return {
        'operation_type': 'WITHDRAW',
        'amount': '300.00'
    }


@pytest.fixture(scope="function")
def withdraw_500():
    return {
        'operation_type': 'WITHDRAW',
        'amount': '500.00'
    }


@pytest.fixture(scope="function")
def deposit_300():
    return {
        'operation_type': 'DEPOSIT',
        'amount': '300.00'
    }


@pytest.fixture(scope="function")
def deposit_500():
    return {
        'operation_type': 'DEPOSIT',
        'amount': '500.00'
    }
