from django.db import transaction
from .emails import send_html_email


def handle_deposit(user, amount):
    account = user.account

    with transaction.atomic():
        account.balance += amount
        account.save(update_fields=['balance'])

        def send_email():
            send_html_email(
                subject="Deposit Successful 💰",
                template="emails/deposit_success.html",
                context={
                    "username": user.username,
                    "amount": amount,
                    "balance": account.balance,
                },
                to_email=user.email,
            )

        transaction.on_commit(send_email)

def handle_withdraw(user, amount):
    account = user.account

    with transaction.atomic():
        account.balance -= amount
        account.save(update_fields=['balance'])

        def send_email():
            send_html_email(
                subject="Withdrawal Successful 💸",
                template="emails/withdraw_success.html",
                context={
                    "username": user.username,
                    "amount": amount,
                    "balance": account.balance,
                },
                to_email=user.email,
            )

        transaction.on_commit(send_email)

def handle_loan_request(user, amount):
    account = user.account

    with transaction.atomic():

        def send_email():
            send_html_email(
                subject="Loan Request Submitted 📝",
                template="emails/loan_request.html",
                context={
                    "username": user.username,
                    "amount": amount,
                },
                to_email=user.email,
            )

        transaction.on_commit(send_email)

def handle_loan_approval(transaction_obj):
    account = transaction_obj.account
    user = account.user
    amount = transaction_obj.amount

    with transaction.atomic():
        account.balance += amount
        account.save(update_fields=['balance'])

        transaction_obj.loan_approved = True
        transaction_obj.balance_after_transaction = account.balance
        transaction_obj.save(update_fields=['loan_approved', 'balance_after_transaction'])

        def send_email():
            send_html_email(
                subject="Loan Approved ✅",
                template="emails/loan_approved.html",
                context={
                    "username": user.username,
                    "amount": amount,
                    "balance": account.balance,
                },
                to_email=user.email,
            )

        transaction.on_commit(send_email)