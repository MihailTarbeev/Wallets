from django.forms import model_to_dict
from rest_framework import generics
from wallets.serializers import WalletSerializer
from .models import Wallet
from rest_framework.views import APIView
from rest_framework.response import Response


# class WalletAPIView(generics.ListAPIView):
#     queryset = Wallet.objects.all()
#     serializer_class = WalletSerializer


class WalletAPIView(APIView):
    def get(self, request):
        lst = Wallet.objects.all().values()
        return Response({'Кошельки': list(lst)})

    def post(self, request):
        new_wallet = Wallet.objects.create(
            balance=request.data['balance']
        )
        return Response({'Кошелёк': model_to_dict(new_wallet)})
