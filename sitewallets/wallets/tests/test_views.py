import pytest
import json
from decimal import Decimal
from django.urls import reverse
from wallets.models import Operation, Wallet
import uuid


class TestWalletAPI:
    """Тесты API кошельков"""

    @pytest.mark.django_db
    def test_get_wallet_balance(self, authenticated_api_client, temp_wallet_1000):
        """Тест получения баланса кошелька"""
        url = reverse('wallet-detail', kwargs={'pk': temp_wallet_1000.uuid})
        response = authenticated_api_client.get(url)

        assert response.status_code == 200
        data = response.json()
        assert Decimal(data['balance']) == temp_wallet_1000.balance

    @pytest.mark.django_db
    def test_get_nonexistent_wallet(self, authenticated_api_client):
        """Тест получения несуществующего кошелька"""
        fake_uuid = uuid.uuid4()
        url = reverse('wallet-detail', kwargs={'pk': fake_uuid})
        response = authenticated_api_client.get(url)

        assert response.status_code == 404

    @pytest.mark.django_db
    def test_deposit_operation(self, authenticated_api_client, temp_wallet_1000, deposit_500):
        """Тест операции пополнения"""
        url = reverse('wallet-operation', kwargs={'pk': temp_wallet_1000.uuid})

        response = authenticated_api_client.post(
            url,
            data=json.dumps(deposit_500),
            content_type='application/json'
        )

        assert response.status_code == 200
        response_data = response.json()
        temp_wallet_1000.refresh_from_db()

        assert temp_wallet_1000.balance == Decimal('1500.00')
        assert response_data['wallet']['uuid'] == str(temp_wallet_1000.uuid)
        assert Decimal(response_data['wallet']
                       ['balance']) == Decimal('1500.00')
        assert response_data['operation']['operation_type'] == 'DEPOSIT'
        assert Decimal(response_data['operation']
                       ['amount']) == Decimal('500.00')
        assert Operation.objects.filter(wallet=temp_wallet_1000).count() == 1

    @pytest.mark.django_db
    def test_withdraw_operation(self, authenticated_api_client, temp_wallet_1000, withdraw_300):
        """Тест операции списания"""
        url = reverse('wallet-operation', kwargs={'pk': temp_wallet_1000.uuid})

        response = authenticated_api_client.post(
            url,
            data=json.dumps(withdraw_300),
            content_type='application/json'
        )

        assert response.status_code == 200

        temp_wallet_1000.refresh_from_db()
        assert temp_wallet_1000.balance == Decimal('700.00')

    @pytest.mark.django_db
    def test_withdraw_insufficient_funds(self, authenticated_api_client, temp_wallet_default, withdraw_300):
        """Тест списания при недостатке средств"""
        url = reverse('wallet-operation',
                      kwargs={'pk': temp_wallet_default.uuid})

        response = authenticated_api_client.post(
            url,
            data=json.dumps(withdraw_300),
            content_type='application/json'
        )

        assert response.status_code in [400, 422]

        temp_wallet_default.refresh_from_db()
        assert temp_wallet_default.balance == Decimal('0.00')

    @pytest.mark.django_db
    def test_idempotent_operation(self, authenticated_api_client, temp_wallet_1000, deposit_300):
        """Тест идемпотентности операций"""
        import uuid

        transaction_id = uuid.uuid4()
        url = reverse('wallet-operation', kwargs={'pk': temp_wallet_1000.uuid})

        deposit_300["transaction_id"] = str(transaction_id)

        response1 = authenticated_api_client.post(
            url,
            data=json.dumps(deposit_300),
            content_type='application/json'
        )
        assert response1.status_code == 200

        response2 = authenticated_api_client.post(
            url,
            data=json.dumps(deposit_300),
            content_type='application/json'
        )

        assert response2.status_code in [200, 400, 409]

        operations_count = Operation.objects.filter(
            wallet=temp_wallet_1000,
            transaction_id=transaction_id
        ).count()

        assert operations_count == 1

    @pytest.mark.django_db
    def test_race_condition_protection(self, authenticated_api_client, temp_wallet_1000, deposit_500):
        """Упрощенный тест защиты от race conditions"""
        wallet_uuid = temp_wallet_1000.uuid

        url = reverse('wallet-operation', kwargs={'pk': wallet_uuid})

        response1 = authenticated_api_client.post(
            url,
            data=json.dumps(deposit_500),
            content_type='application/json'
        )

        response2 = authenticated_api_client.post(
            url,
            data=json.dumps(deposit_500),
            content_type='application/json'
        )

        assert response1.status_code == 200, f"Первый запрос завершился с статусом {response1.status_code}"
        assert response2.status_code == 200, f"Второй запрос завершился с статусом {response2.status_code}"

        temp_wallet_1000.refresh_from_db()
        assert temp_wallet_1000.balance == Decimal('2000.00')

        operation_count = Operation.objects.filter(
            wallet=temp_wallet_1000).count()
        assert operation_count == 2

    @pytest.mark.django_db
    def test_get_wallets_list_empty(self, authenticated_api_client):
        """Тест получения пустого списка кошельков"""
        url = reverse('wallet-list')
        response = authenticated_api_client.get(url)

        assert response.status_code == 200
        assert response.json() == []

    @pytest.mark.django_db
    def test_get_wallets_list_with_data(self, authenticated_api_client, temp_wallet_1000, temp_wallet_default):
        """Тест получения списка кошельков с данными"""
        url = reverse('wallet-list')
        response = authenticated_api_client.get(url)

        assert response.status_code == 200
        data = response.json()

        assert len(data) == 2

        for wallet_data in data:
            assert 'uuid' in wallet_data
            assert 'balance' in wallet_data
            assert isinstance(wallet_data['uuid'], str)
            assert isinstance(wallet_data['balance'], str)

    @pytest.mark.django_db
    def test_create_wallet(self, authenticated_api_client):
        """Тест создания нового кошелька"""
        url = reverse('wallet-list')

        response = authenticated_api_client.post(
            url,
            content_type='application/json'
        )

        assert response.status_code == 201
        response_data = response.json()

        assert 'uuid' in response_data
        assert response_data['balance'] == '0.00'

        wallet = Wallet.objects.get(uuid=response_data['uuid'])
        assert wallet.balance == Decimal('0.00')

    @pytest.mark.django_db
    def test_get_operations_list_empty(self, authenticated_api_client):
        """Тест получения пустого списка операций"""
        url = reverse('operation-list')
        response = authenticated_api_client.get(url)

        assert response.status_code == 200
        data = response.json()
        assert data == []

    @pytest.mark.django_db
    def test_get_operations_list_with_data(self, authenticated_api_client, temp_operation_dep_100, temp_operation_wid_500):
        """Тест получения списка операций с данными"""
        url = reverse('operation-list')
        response = authenticated_api_client.get(url)

        assert response.status_code == 200
        data = response.json()

        assert len(data) == 2
