from django.urls import path
from wallets.views import WalletAPIList, WalletAPIGet, WalletAPIUpdate, OperationAPIList

urlpatterns = [
    path('wallets/', WalletAPIList.as_view()),
    path('operations/', OperationAPIList.as_view()),
    path('wallets/<uuid:pk>/', WalletAPIGet.as_view()),
    path('wallets/<uuid:pk>/operation', WalletAPIUpdate.as_view()),
]
