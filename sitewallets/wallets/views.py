from rest_framework import generics
from wallets.serializers import WalletSerializer
from .models import Wallet


class WalletAPIView(generics.ListAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
