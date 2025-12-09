import pytest
from django.test import Client
from wallets.models import Wallet, Operation
from decimal import Decimal
import uuid


@pytest.fixture
def api_client():
    return Client()


@pytest.fixture(scope="function")
def temp_wallet_default():
    wallet = Wallet.objects.create()
    return wallet


@pytest.fixture(scope="function")
def temp_wallet_1000():
    wallet = Wallet.objects.create(balance=Decimal('1000.00'))
    return wallet


@pytest.fixture(scope="function")
def temp_operation_dep_100(temp_wallet_1000):
    operation = Operation.objects.create(
        transaction_id=uuid.uuid4(),
        operation_type='DEPOSIT',
        amount=Decimal('100.00'),
        wallet=temp_wallet_1000
    )
    return operation


@pytest.fixture(scope="function")
def temp_operation_wid_500(temp_wallet_1000):
    operation = Operation.objects.create(
        transaction_id=uuid.uuid4(),
        operation_type='WITHDRAW',
        amount=Decimal('500.00'),
        wallet=temp_wallet_1000
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
