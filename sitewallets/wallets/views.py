from django.forms import model_to_dict
from rest_framework import generics, viewsets, mixins
from rest_framework.viewsets import GenericViewSet
from wallets.serializers import WalletSerializer
from .models import Wallet
from rest_framework.views import APIView
from rest_framework.response import Response


# class WalletAPIList(generics.ListCreateAPIView):
#     queryset = Wallet.objects.all()
#     serializer_class = WalletSerializer


# class WalletAPIUpdate(generics.UpdateAPIView):
#     queryset = Wallet.objects.all()
#     serializer_class = WalletSerializer


# class WalletAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Wallet.objects.all()
#     serializer_class = WalletSerializer


class WalletViewSet(mixins.CreateModelMixin,
                    mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.ListModelMixin,
                    GenericViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
