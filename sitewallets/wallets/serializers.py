import io
from rest_framework import serializers
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Wallet
import uuid


class WalletSerializer(serializers.Serializer):
    uuid = serializers.UUIDField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    balance = serializers.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0.00)
