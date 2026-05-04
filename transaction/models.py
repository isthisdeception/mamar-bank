from django.db import models
from accounts.models import UserBankAccount

# Use a TextChoices class for better readability and type safety
class TransactionType(models.TextChoices):
    DEPOSIT = 'DEPOSIT', 'Deposit'
    WITHDRAWAL = 'WITHDRAWAL', 'Withdrawal'
    LOAN = 'LOAN', 'Loan Request'
    LOAN_REPAY = 'LOAN_REPAY', 'Loan Repayment'

class Transaction(models.Model):
    account = models.ForeignKey(
        UserBankAccount, 
        on_delete=models.CASCADE, 
        related_name='transactions'
    )
    # Use DecimalField for all financial data to avoid floating-point errors
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after_transaction = models.DecimalField(max_digits=12, decimal_places=2)
    
    transaction_type = models.CharField(
        max_length=20, 
        choices=TransactionType.choices,
        db_index=True  # Indexing type for faster report filtering
    )
    
    # auto_now_add is standard for creation timestamps
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    loan_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-timestamp']
        # Adding indexes makes the "Report" feature much faster as data grows
        indexes = [
            models.Index(fields=['account', '-timestamp']),
        ]

    def __str__(self):
        return f"{self.account.user.username} - {self.transaction_type} - {self.amount}"