from django.contrib.auth.models import User
from django.db import models
import uuid


class Wallet(models.Model):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        unique=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    balance = models.DecimalField(
        max_digits=20,
        decimal_places=2,
        default=0.00
    )
    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE)

    class Meta:
        db_table = 'wallets'
        ordering = ['-created_at']

    def __str__(self):
        return f"Wallet {self.uuid}"


class Operation(models.Model):
    class OperationType(models.TextChoices):
        DEPOSIT = 'DEPOSIT', 'Пополнение'
        WITHDRAW = 'WITHDRAW', 'Снятие'

    transaction_id = models.UUIDField(
        null=True,
        blank=True,
        unique=True
    )
    operation_type = models.CharField(
        max_length=10,
        choices=OperationType.choices
    )
    amount = models.DecimalField(
        max_digits=20,
        decimal_places=2
    )
    wallet = models.ForeignKey(
        Wallet,
        on_delete=models.PROTECT,
        related_name='operations'
    )

    created_at = models.DateTimeField(auto_now_add=True)

    user = models.ForeignKey(
        User, verbose_name='Пользователь', on_delete=models.CASCADE)

    class Meta:
        db_table = 'operations'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['wallet', 'created_at']),
            models.Index(fields=['transaction_id']),
        ]

    def __str__(self):
        return f"{self.operation_type} {self.amount} to {self.wallet.uuid}"
