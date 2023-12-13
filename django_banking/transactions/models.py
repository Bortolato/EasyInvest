from django.db import models


from .constants import TRANSACTION_TYPE_CHOICES, OPERATION_TYPE_CHOICES, TIPOS_ATIVOS
from accounts.models import UserBankAccount


class Transaction(models.Model):
    account = models.ForeignKey(
        UserBankAccount,
        related_name='transactions',
        on_delete=models.CASCADE,
    )
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12
    )
    balance_after_transaction = models.DecimalField(
        decimal_places=2,
        max_digits=12
    )
    transaction_type = models.PositiveSmallIntegerField(
        choices=TRANSACTION_TYPE_CHOICES
    )
    operation_type = models.PositiveSmallIntegerField(
        choices=OPERATION_TYPE_CHOICES
    )
    tipo_ativo = models.PositiveSmallIntegerField(
        choices=TIPOS_ATIVOS
    )
    additional_text = models.CharField(max_length=255, blank=True, null=True)  # Novo campo adicionado
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.account.account_no)

    class Meta:
        ordering = ['timestamp']



class Ativo(models.Model):
    # Campos relacionados ao ativo
    nome = models.CharField(max_length=255, help_text='Nome do ativo')
    tipo  = models.PositiveSmallIntegerField(
        choices=TIPOS_ATIVOS
    )
    descricao = models.TextField(blank=True, null=True, help_text='Descrição detalhada do ativo')
    preco_atual = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text='Preço atual do ativo')
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nome