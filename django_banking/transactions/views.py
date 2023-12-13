from dateutil.relativedelta import relativedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView
from django.shortcuts import render, redirect

from transactions.constants import DEPOSIT, WITHDRAWAL
from transactions.forms import (
    DepositForm,
    TransactionDateRangeForm,
    WithdrawForm,
    AtivoForm,
    AtivoDateRangeForm
)
from transactions.models import Transaction, Ativo


class TransactionRepostView(LoginRequiredMixin, ListView):
    template_name = 'transactions/transaction_report.html'
    model = Transaction
    form_data = {}

    def get(self, request, *args, **kwargs):
        form = TransactionDateRangeForm(request.GET or None)
        if form.is_valid():
            self.form_data = form.cleaned_data

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset().filter(
            account=self.request.user.account
        )

        daterange = self.form_data.get("daterange")

        if daterange:
            queryset = queryset.filter(timestamp__date__range=daterange)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'account': self.request.user.account,
            'form': TransactionDateRangeForm(self.request.GET or None)
        })

        return context
    

class AssetReportView(LoginRequiredMixin, ListView):
    template_name = 'transactions/asset_report.html'
    model = Ativo
    form_data = {}

    def get(self, request, *args, **kwargs):
        form = AtivoDateRangeForm(request.GET or None)  # Corrigido para AtivoDateRangeForm
        if form.is_valid():
            self.form_data = form.cleaned_data

        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset().filter(
        )

        daterange = self.form_data.get("daterange")

        if daterange:
            queryset = queryset.filter(timestamp__date__range=daterange)

        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'form': AtivoDateRangeForm(self.request.GET or None)  # Corrigido para AtivoDateRangeForm
        })

        return context
    

class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transactions/transaction_form.html'
    model = Transaction
    title = ''
    success_url = reverse_lazy('transactions:transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account
        })
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'title': self.title
        })

        return context


class DepositMoneyView(TransactionCreateMixin):
    form_class = DepositForm
    title = 'Criar um novo Ativo'

    def get_initial(self):
        initial = {'transaction_type': DEPOSIT}
        return initial

    def form_valid(self, form):
        # import pdb; pdb.set_trace()
        amount = form.cleaned_data.get('amount')
        operation_type = form.cleaned_data.get('operation_type')
        tipo_ativo = form.cleaned_data.get('tipo_ativo')
        additional_text = form.cleaned_data.get('additional_text')
        account = self.request.user.account

        if not account.initial_deposit_date:
            now = timezone.now()
            next_interest_month = int(
                12 / account.account_type.interest_calculation_per_year
            )
            account.initial_deposit_date = now
            account.interest_start_date = (
                now + relativedelta(
                    months=+next_interest_month
                )
            )

        account.balance += amount
        account.save(
            update_fields=[
                'initial_deposit_date',
                'balance',
                'interest_start_date'
            ]
        )

        messages.success(
            self.request,
            'Operação criada com sucesso!'
        )

        return super().form_valid(form)


class WithdrawMoneyView(TransactionCreateMixin):
    form_class = WithdrawForm
    title = 'Criar uma nova operação'

    def get_initial(self):
        initial = {'transaction_type': WITHDRAWAL}
        return initial

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        operation_type = form.cleaned_data.get('operation_type')
        if operation_type == 4:
            self.request.user.account.balance += amount
        else:
            self.request.user.account.balance -= amount
            
        self.request.user.account.save(update_fields=['balance'])

        messages.success(
            self.request,
            'Operação criada com sucesso!'
        )

        return super().form_valid(form)


def criar_ativo(request):
    if request.method == 'POST':
        form = AtivoForm(request.POST)
        if form.is_valid():
            form.save()

            # Adicione a mensagem de sucesso
            messages.success(
                request,
                'Ativo criado com sucesso!'
            )
            return redirect('transactions:asset_report')  # Redireciona para a página de lista de ativos (ajuste conforme necessário)
    else:
        form = AtivoForm()

    return render(request, 'transactions/asset_form.html', {'form': form, 'title': 'Criar um novo Ativo'})