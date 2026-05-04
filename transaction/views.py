from django.db import transaction
from django.views.generic import CreateView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Transaction, TransactionType
from .forms import TransactionForm, DateRangeForm
from .services import handle_deposit, handle_withdraw, handle_loan_request

# --- 1. Transaction Report ---
class TransactionReportView(LoginRequiredMixin, ListView):
    template_name = 'transaction/report.html'
    model = Transaction
    context_object_name = 'transactions'

    def get_queryset(self):
        queryset = super().get_queryset().filter(account=self.request.user.account)
        start_date_str = self.request.GET.get('start_date')
        end_date_str = self.request.GET.get('end_date')
        
        if start_date_str and end_date_str:
            queryset = queryset.filter(timestamp__date__range=[start_date_str, end_date_str])
        
        # Only show loans if they are approved
        return queryset.exclude(transaction_type=TransactionType.LOAN, loan_approved=False)

# --- 2. Deposit & 3. Withdrawal (Base Logic) ---
class TransactionCreateMixin(LoginRequiredMixin, CreateView):
    template_name = 'transaction/transaction_form.html'
    model = Transaction
    form_class = TransactionForm
    success_url = reverse_lazy('transaction_report')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({
            'account': self.request.user.account,
            'transaction_type': self.transaction_type,
        })
        return kwargs

    def form_valid(self, form):
        amount = form.cleaned_data.get('amount')
        account = self.request.user.account
        
        with transaction.atomic():
            # 1. Handle Withdrawal
            if self.transaction_type == TransactionType.WITHDRAWAL:
                handle_withdraw(self.request.user, amount)

            # 2. Handle Deposit
            elif self.transaction_type == TransactionType.DEPOSIT:
                handle_deposit(self.request.user, amount)

            # 3. Handle Loan Request (balance unchanged until admin approves)
            elif self.transaction_type == TransactionType.LOAN:
                form.instance.loan_approved = False
                handle_loan_request(self.request.user, amount)

            # Prepare the transaction record
            form.instance.account = account
            form.instance.balance_after_transaction = account.balance
            form.instance.transaction_type = self.transaction_type
            
            if self.transaction_type == TransactionType.LOAN:
                messages.success(self.request, "Loan request submitted to Admin.")
            else:
                messages.success(self.request, "Transaction successfully submitted.")
            if not self.request.user.email:
                messages.warning(
                    self.request,
                    "No email is set on your profile, so notification email was not sent.",
                )
            return super().form_valid(form)

class DepositMoneyView(TransactionCreateMixin):
    transaction_type = TransactionType.DEPOSIT

class WithdrawMoneyView(TransactionCreateMixin):
    transaction_type = TransactionType.WITHDRAWAL

# --- 4. Loan Request ---
class LoanRequestView(TransactionCreateMixin):
    transaction_type = TransactionType.LOAN