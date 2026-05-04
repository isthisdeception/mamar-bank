from django.db import models
from .constants import ACCOUNT_TYPE_CHOICES, GENDER_CHOICES
from django.contrib.auth.models import User

class UserBankAccount(models.Model):
    user = models.OneToOneField(
        User, 
        related_name='account', 
        on_delete=models.CASCADE
    )
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPE_CHOICES)
    account_no = models.PositiveIntegerField(unique=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    initial_deposit_date = models.DateField(auto_now_add=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def __str__(self):
        return f"{self.user} - {self.account_no}"


class UserAddress(models.Model):
    user = models.OneToOneField(
        User, 
        related_name='user_address', 
        on_delete=models.CASCADE
    )
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)