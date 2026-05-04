from django import forms
from .models import Transaction, TransactionType

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount']

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account', None)
        self.transaction_type = kwargs.pop('transaction_type', None)
        super().__init__(*args, **kwargs)

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if amount <= 0:
            raise forms.ValidationError("Amount must be greater than zero.")

        if (
            self.transaction_type == TransactionType.WITHDRAWAL
            and self.account
            and amount > self.account.balance
        ):
            raise forms.ValidationError("Insufficient funds for this withdrawal.")

        return amount

class DateRangeForm(forms.Form):
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))