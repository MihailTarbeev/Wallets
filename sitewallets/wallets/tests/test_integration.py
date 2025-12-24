import pytest
import json
from decimal import Decimal
from django.urls import reverse
from wallets.models import Operation


@pytest.mark.django_db
class TestWalletIntegration:
    """Интеграционные тесты полного цикла операций"""

    def test_complete_wallet_flow(self, authenticated_api_client, temp_wallet_1000, deposit_500, withdraw_300):
        """Полный тестовый сценарий работы с кошельком"""

        url = reverse('wallet-detail', kwargs={'pk': temp_wallet_1000.uuid})
        response = authenticated_api_client .get(url)
        assert response.status_code == 200
        assert Decimal(response.json()['balance']) == Decimal('1000.00')

        operation_url = reverse(
            'wallet-operation', kwargs={'pk': temp_wallet_1000.uuid})

        response = authenticated_api_client .post(
            operation_url,
            data=json.dumps(deposit_500),
            content_type='application/json'
        )
        assert response.status_code == 200

        temp_wallet_1000.refresh_from_db()
        assert temp_wallet_1000.balance == Decimal('1500.00')

        response = authenticated_api_client .post(
            operation_url,
            data=json.dumps(withdraw_300),
            content_type='application/json'
        )
        assert response.status_code == 200

        temp_wallet_1000.refresh_from_db()
        assert temp_wallet_1000.balance == Decimal('1200.00')

        operations = Operation.objects.filter(wallet=temp_wallet_1000)
        assert operations.count() == 2

        deposit_ops = operations.filter(operation_type='DEPOSIT')
        withdraw_ops = operations.filter(operation_type='WITHDRAW')

        assert deposit_ops.count() == 1
        assert withdraw_ops.count() == 1

        assert deposit_ops.first().amount == Decimal('500.00')
        assert withdraw_ops.first().amount == Decimal('300.00')
