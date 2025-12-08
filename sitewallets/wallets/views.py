from django.forms import model_to_dict
from rest_framework import generics
from wallets.serializers import WalletSerializer
from .models import Wallet
from rest_framework.views import APIView
from rest_framework.response import Response


class WalletAPIList(generics.ListCreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class WalletAPIUpdate(generics.UpdateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


class WalletAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer


# class WalletAPIView(APIView):
#     def get(self, request):
#         wallets_objs = Wallet.objects.all()
#         return Response({'wallets': WalletSerializer(wallets_objs, many=True).data})

#     def post(self, request):
#         serializer = WalletSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         # метод save вызывает в WalletSerializer метод create
#         serializer.save()

#         return Response({'wallet': serializer.data})

#     def put(self, request,  *args, **kwargs):
#         uuid = kwargs.get("uuid", None)
#         if not uuid:
#             return Response({"error": "Method PUT not allowed"})

#         try:
#             instance = Wallet.objects.get(uuid=uuid)
#         except:
#             return Response({"error": "Object does not exists"})

#         serializer = WalletSerializer(data=request.data, instance=instance)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response({"wallet": serializer.data})
