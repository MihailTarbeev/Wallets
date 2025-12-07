from django.forms import model_to_dict
from rest_framework import generics
from wallets.serializers import WalletSerializer
from .models import Wallet
from rest_framework.views import APIView
from rest_framework.response import Response


class WalletAPIView(APIView):
    def get(self, request):
        wallets_objs = Wallet.objects.all()
        return Response({'wallets': WalletSerializer(wallets_objs, many=True).data})

    def post(self, request):
        serializer = WalletSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_wallet = Wallet.objects.create(
            balance=request.data['balance']
        )
        return Response({'wallet': WalletSerializer(new_wallet).data})
