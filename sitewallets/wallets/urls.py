from django.urls import path
from wallets.views import WalletAPIList, WalletAPIGet, WalletAPIUpdate, OperationAPIList

urlpatterns = [
    path('wallets/', WalletAPIList.as_view(), name='wallet-list'),
    path('operations/', OperationAPIList.as_view(), name='operation-list'),
    path('wallets/<uuid:pk>/', WalletAPIGet.as_view(), name='wallet-detail'),
    path('wallets/<uuid:pk>/operation',
         WalletAPIUpdate.as_view(), name='wallet-operation'),
]
