from django.urls import path
from .views import (
    TransactionReportView, 
    DepositMoneyView, 
    WithdrawMoneyView, 
    LoanRequestView
)

urlpatterns = [
    path("report/", TransactionReportView.as_view(), name="transaction_report"),
    path("deposit/", DepositMoneyView.as_view(), name="deposit_money"),
    path("withdraw/", WithdrawMoneyView.as_view(), name="withdraw_money"),
    path("loan_request/", LoanRequestView.as_view(), name="loan_request"),
]