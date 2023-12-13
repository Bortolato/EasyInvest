import datetime

from django import forms
from django.conf import settings

from .models import Transaction, Ativo

from .constants import TRANSACTION_TYPE_CHOICES, OPERATION_TYPE_CHOICES, TIPOS_ATIVOS


class TransactionForm(forms.ModelForm):

    class Meta:
        model = Transaction
        fields = [
            'amount',
            'transaction_type',
            'operation_type',
            'tipo_ativo',
            'additional_text'
        ]

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)

        self.fields['transaction_type'].disabled = True
        self.fields['transaction_type'].widget = forms.HiddenInput()

    def save(self, commit=True):
        self.instance.account = self.account
        self.instance.balance_after_transaction = self.account.balance
        return super().save()


class DepositForm(TransactionForm):

    operation_type = forms.ChoiceField(choices=OPERATION_TYPE_CHOICES, required=True, label='operation_type')
    tipo_ativo = forms.ChoiceField(choices=TIPOS_ATIVOS, required=True, label='tipo_ativo')
    additional_text = forms.CharField(max_length=255, required=False, label='additional_text')
    
    def clean_amount(self):
        min_deposit_amount = settings.MINIMUM_DEPOSIT_AMOUNT
        amount = self.cleaned_data.get('amount')

        if amount < min_deposit_amount:
            raise forms.ValidationError(
                f'You need to deposit at least {min_deposit_amount} $'
            )

        return amount


class WithdrawForm(TransactionForm):

    def clean_amount(self):
        account = self.account
        min_withdraw_amount = settings.MINIMUM_WITHDRAWAL_AMOUNT
        max_withdraw_amount = (
            account.account_type.maximum_withdrawal_amount
        )
        balance = account.balance

        amount = self.cleaned_data.get('amount')

        return amount


class TransactionDateRangeForm(forms.Form):
    daterange = forms.CharField(required=False)

    def clean_daterange(self):
        daterange = self.cleaned_data.get("daterange")
        print(daterange)

        try:
            daterange = daterange.split(' - ')
            print(daterange)
            if len(daterange) == 2:
                for date in daterange:
                    datetime.datetime.strptime(date, '%Y-%m-%d')
                return daterange
            else:
                raise forms.ValidationError("Por favor, selecione um intervalo de datas.")
        except (ValueError, AttributeError):
            raise forms.ValidationError("Intervalo de datas inválido")


class AtivoForm(forms.ModelForm):
    tipo_ativo = forms.ChoiceField(choices=TIPOS_ATIVOS, required=True, label='Tipo de Ativo')

    class Meta:
        model = Ativo
        fields = ['nome', 'descricao', 'preco_atual']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)    

        self.fields['descricao'].widget = forms.Textarea(attrs={'rows': 4})
        self.fields['preco_atual'].widget.attrs.update({'step': '0.01'})
        self.fields['nome'].widget.attrs.update({'class': 'form-control'})

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.tipo = self.cleaned_data.get('tipo_ativo')  # Atribua o valor do tipo_ativo ao campo tipo do modelo Ativo

        if commit:
            instance.save()


class AtivoDateRangeForm(forms.Form):
    daterange = forms.CharField(required=False)

    def clean_daterange(self):
        daterange = self.cleaned_data.get("daterange")

        try:
            daterange = daterange.split(' - ')
            if len(daterange) == 2:
                for date in daterange:
                    datetime.datetime.strptime(date, '%Y-%m-%d')
                return daterange
            else:
                raise forms.ValidationError("Por favor, selecione um intervalo de datas.")
        except (ValueError, AttributeError):
            raise forms.ValidationError("Intervalo de datas inválido")