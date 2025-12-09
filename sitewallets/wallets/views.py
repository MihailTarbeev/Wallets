from wallets.serializers import WalletSerializer, OperationSerializer, WalletOperationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
import uuid as uuid_lib
from .models import Wallet, Operation
from .serializers import WalletOperationSerializer, WalletSerializer
from rest_framework.generics import RetrieveAPIView, ListCreateAPIView


class WalletAPIList(ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class OperationAPIList(ListCreateAPIView):
    queryset = Operation.objects.all()
    serializer_class = OperationSerializer


class WalletAPIGet(RetrieveAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class WalletAPIUpdate(APIView):
    def post(self, request, pk, *args, **kwargs):
        try:
            wallet = Wallet.objects.get(uuid=pk)
        except Wallet.DoesNotExist:
            return Response(
                {"error": "Wallet not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = WalletOperationSerializer(
            data=request.data,
            context={'wallet': wallet}
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        operation_type = serializer.validated_data['operation_type']
        amount = serializer.validated_data['amount']
        transaction_id = serializer.validated_data.get(
            'transaction_id') or uuid_lib.uuid4()

        try:
            with transaction.atomic():
                wallet = Wallet.objects.select_for_update(
                    nowait=False).get(uuid=pk)

                if Operation.objects.filter(transaction_id=transaction_id).exists():
                    return Response(
                        {"error": "Дублирование transaction_id"},
                        status=status.HTTP_400_BAD_REQUEST
                    )

                operation = Operation.objects.create(
                    transaction_id=transaction_id,
                    operation_type=operation_type,
                    amount=amount,
                    wallet=wallet
                )

                if operation_type == 'DEPOSIT':
                    wallet.balance += amount
                elif operation_type == 'WITHDRAW':
                    wallet.balance -= amount

                wallet.save()

                return Response(
                    {
                        "wallet": {
                            "uuid": str(wallet.uuid),
                            "balance": str(wallet.balance),
                            "updated_at": wallet.updated_at.isoformat()
                        },
                        "operation": {
                            "transaction_id": str(operation.transaction_id),
                            "operation_type": operation.operation_type,
                            "amount": str(operation.amount),
                            "created_at": operation.created_at.isoformat()
                        }
                    },
                    status=status.HTTP_200_OK
                )

        except Exception as e:
            if 'lock' in str(e).lower() or 'timeout' in str(e).lower():
                return Response(
                    {"error": "Выполняется другая операция, попробуйте снова"},
                    status=status.HTTP_409_CONFLICT
                )
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
