import pytest
import uuid
from decimal import Decimal
from django.db import IntegrityError
from wallets.models import Operation


class TestWalletModel:
    """Тесты модели Wallet"""

    @pytest.mark.django_db
    def test_create_wallet(self, temp_wallet_1000):
        """Тест создания кошелька"""
        assert temp_wallet_1000.balance == Decimal('1000.00')
        assert temp_wallet_1000.uuid is not None

    @pytest.mark.django_db
    def test_wallet_str_method(self, temp_wallet_1000):
        """Тест строкового представления"""
        assert str(temp_wallet_1000) == f"Wallet {temp_wallet_1000.uuid}"

    @pytest.mark.django_db
    def test_default_balance(self, temp_wallet_default):
        """Тест значения по умолчанию для баланса"""
        assert temp_wallet_default.balance == Decimal('0.00')


class TestOperationModel:
    """Тесты модели Operation"""

    @pytest.mark.django_db
    def test_create_operation(self, temp_operation_dep_100):
        """Тест создания операции"""
        assert temp_operation_dep_100.amount == Decimal('100.00')
        assert temp_operation_dep_100.operation_type == 'DEPOSIT'
        assert temp_operation_dep_100.transaction_id is not None

    @pytest.mark.django_db
    def test_operation_str_method(self, temp_operation_wid_500):
        """Тест строкового представления операции"""
        expected = f"WITHDRAW 500.00 to {temp_operation_wid_500.wallet.uuid}"
        assert str(temp_operation_wid_500) == expected

    @pytest.mark.django_db
    def test_unique_transaction_id(self, temp_wallet_1000):
        """Тест уникальности transaction_id"""
        transaction_id = uuid.uuid4()

        Operation.objects.create(
            transaction_id=transaction_id,
            operation_type='DEPOSIT',
            amount=Decimal('100.00'),
            wallet=temp_wallet_1000
        )

        with pytest.raises(IntegrityError):
            Operation.objects.create(
                transaction_id=transaction_id,
                operation_type='DEPOSIT',
                amount=Decimal('200.00'),
                wallet=temp_wallet_1000
            )
