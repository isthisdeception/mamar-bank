from django.contrib import admin
from .models import Transaction, TransactionType
from .services import handle_loan_approval


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['account', 'amount', 'balance_after_transaction', 'transaction_type', 'loan_approved']

    def save_model(self, request, obj, form, change):
        if (
            change
            and obj.transaction_type == TransactionType.LOAN
            and obj.loan_approved
        ):
            prior = Transaction.objects.get(pk=obj.pk)
            if not prior.loan_approved:
                handle_loan_approval(obj)
        super().save_model(request, obj, form, change)