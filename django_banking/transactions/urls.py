from django.urls import path

from .views import DepositMoneyView, WithdrawMoneyView, TransactionRepostView, criar_ativo, AssetReportView


app_name = 'transactions'


urlpatterns = [
    path("deposit/", DepositMoneyView.as_view(), name="deposit_money"),
    path("report/", TransactionRepostView.as_view(), name="transaction_report"),
    path("withdraw/", WithdrawMoneyView.as_view(), name="withdraw_money"),
    path("createAssset/", criar_ativo, name="create_asset"),
    path("asset/", AssetReportView.as_view(), name="asset_report")
]
