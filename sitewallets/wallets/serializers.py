from rest_framework import serializers
from .models import Wallet, Operation
from decimal import Decimal


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = "__all__"
        read_only_fields = ('user', 'uuid', 'created_at',
                            'updated_at', 'balance')
        extra_kwargs = {
            'balance': {'min_value': Decimal('0.00'), 'read_only': True}
        }


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = ("created_at", "wallet", "operation_type",
                  "amount", "transaction_id", "user")
        read_only_fields = ('user', 'transaction_id', 'created_at')


class WalletOperationSerializer(serializers.Serializer):
    operation_type = serializers.ChoiceField(
        choices=['DEPOSIT', 'WITHDRAW'],
        required=True
    )
    amount = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
        min_value=Decimal('0.01'),
        required=True
    )
    transaction_id = serializers.UUIDField(required=False)

    def validate(self, data):
        wallet = self.context.get('wallet')
        if not wallet:
            raise serializers.ValidationError("Wallet not found")

        if data['operation_type'] == 'WITHDRAW':
            if wallet.balance < data['amount']:
                raise serializers.ValidationError(
                    {"amount": "Недостаточно средств"}
                )

        transaction_id = data.get('transaction_id')
        if transaction_id:
            if Operation.objects.filter(transaction_id=transaction_id).exists():
                raise serializers.ValidationError(
                    {"transaction_id": "transaction_id должно быть уникальным"}
                )

        return data
