import pytest
import uuid
from decimal import Decimal
from wallets.serializers import WalletSerializer, WalletOperationSerializer
from wallets.models import Wallet, Operation


class TestWalletSerializer:
    """Тесты сериализатора Wallet"""

    @pytest.mark.django_db
    def test_wallet_serialization(self, temp_wallet_1000):
        """Тест сериализации кошелька"""
        serializer = WalletSerializer(temp_wallet_1000)

        data = serializer.data
        assert data['uuid'] == str(temp_wallet_1000.uuid)
        assert Decimal(data['balance']) == Decimal('1000.00')


class TestWalletOperationSerializer:
    """Тесты сериализатора операций"""

    @pytest.mark.django_db
    def test_valid_deposit_operation(self, temp_wallet_1000):
        """Тест валидной операции пополнения"""
        data = {
            'operation_type': 'DEPOSIT',
            'amount': '500.00'
        }

        serializer = WalletOperationSerializer(
            data=data,
            context={'wallet': temp_wallet_1000}
        )

        assert serializer.is_valid() is True

    @pytest.mark.django_db
    def test_valid_withdraw_operation(self, temp_wallet_1000):
        """Тест валидной операции списания"""
        data = {
            'operation_type': 'WITHDRAW',
            'amount': '500.00'
        }

        serializer = WalletOperationSerializer(
            data=data,
            context={'wallet': temp_wallet_1000}
        )

        assert serializer.is_valid() is True

    @pytest.mark.django_db
    def test_invalid_withdraw_insufficient_funds(self, temp_wallet_1000):
        """Тест списания при недостатке средств"""
        data = {
            'operation_type': 'WITHDRAW',
            'amount': '1001.00'
        }

        serializer = WalletOperationSerializer(
            data=data,
            context={'wallet': temp_wallet_1000}
        )

        assert serializer.is_valid() is False
        assert 'amount' in serializer.errors

    @pytest.mark.django_db
    def test_invalid_amount(self, temp_wallet_1000):
        """Тест невалидной суммы"""
        data = {
            'operation_type': 'DEPOSIT',
            'amount': '0.00'
        }

        serializer = WalletOperationSerializer(
            data=data,
            context={'wallet': temp_wallet_1000}
        )

        assert serializer.is_valid() is False

    @pytest.mark.django_db
    def test_duplicate_transaction_id(self, temp_wallet_1000, test_user):
        """Тест уникальности transaction_id"""
        transaction_id = uuid.uuid4()

        Operation.objects.create(
            transaction_id=transaction_id,
            operation_type='DEPOSIT',
            amount=Decimal('100.00'),
            wallet=temp_wallet_1000,
            user=test_user
        )

        data = {
            'operation_type': 'DEPOSIT',
            'amount': '200.00',
            'transaction_id': str(transaction_id)
        }

        serializer = WalletOperationSerializer(
            data=data,
            context={'wallet': temp_wallet_1000}
        )

        assert serializer.is_valid() is False
        assert 'transaction_id' in serializer.errors
