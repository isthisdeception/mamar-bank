from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserBankAccount, UserAddress
from .constants import ACCOUNT_TYPE_CHOICES, GENDER_CHOICES

# 1. Rename your class to avoid shadowing the imported UserCreationForm
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE_CHOICES)
    account_no = forms.IntegerField()
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    initial_deposit_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    balance = forms.DecimalField(initial=0)
    
    street_address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=20)
    country = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'account_type', 'account_no', 'birth_date', 'gender', 'initial_deposit_date', 'balance', 'street_address', 'city', 'postal_code', 'country']

    def save(self, commit=True):
        user = super().save(commit=False) 
        if commit:
            user.save()
            
            # 2. Save the Bank Account linked to this new User
            bank_account = UserBankAccount.objects.create(
                user=user, # Link directly to the user object we just saved
                account_type=self.cleaned_data["account_type"],
                account_no=self.cleaned_data["account_no"],
                birth_date=self.cleaned_data["birth_date"],
                gender=self.cleaned_data["gender"],
                initial_deposit_date=self.cleaned_data["initial_deposit_date"],
                balance=self.cleaned_data["balance"]
            )
            
            # 3. Save the Address linked to the Bank Account
            UserAddress.objects.create(
                user=user, # Linked to the UserBankAccount instance
                street_address=self.cleaned_data["street_address"],
                city=self.cleaned_data["city"],
                postal_code=self.cleaned_data["postal_code"],
                country=self.cleaned_data["country"]
            )
        return user


# user update form
class UserUpdateForm(forms.ModelForm):
    # Displayed but disabled fields
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_CHOICES)
    street_address = forms.CharField(max_length=255)
    city = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=20)
    country = forms.CharField(max_length=100)

    # Read-only fields (Information only)
    account_no = forms.IntegerField(required=False)
    account_type = forms.CharField(required=False)
    balance = forms.DecimalField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate and disable all non-user editable fields
        for field_name in [
            'birth_date',
            'gender',
            'street_address',
            'city',
            'postal_code',
            'country',
            'account_no',
            'account_type',
            'balance',
        ]:
            self.fields[field_name].disabled = True

        if hasattr(self.instance, 'user_bank_account'):
            acc = self.instance.user_bank_account
            self.fields['account_no'].initial = acc.account_no
            self.fields['account_type'].initial = acc.account_type
            self.fields['balance'].initial = acc.balance
            self.fields['birth_date'].initial = acc.birth_date
            self.fields['gender'].initial = acc.gender

        if hasattr(self.instance, 'user_address'):
            addr = self.instance.user_address
            self.fields['street_address'].initial = addr.street_address
            self.fields['city'].initial = addr.city
            self.fields['postal_code'].initial = addr.postal_code
            self.fields['country'].initial = addr.country

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user