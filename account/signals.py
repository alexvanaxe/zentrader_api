from django.db.models.signals import post_save
from django.dispatch import receiver

from operation.models import BuyData, SellData
from stock.models import Stock
from account.models import Account


@receiver(post_save, sender=BuyData)
def debit_account(sender, instance, created, **kwargs):
    if created:
        account = instance.account
        account.equity = account.equity - instance.average_cost()
        account.save()
        account_list = Account.objects.all()
        for account in account_list:
            account.clean_cache()


@receiver(post_save, sender=SellData)
def credit_account(sender, instance, created, **kwargs):
    if instance.executed:
        account = instance.account
        account.equity = account.equity + instance.sell_value()
        account.save()
        account_list = Account.objects.all()
        for account in account_list:
            account.clean_cache()


@receiver(post_save, sender=Stock)
def update_total_equity_cache(sender, instance, created, **kwargs):
    account_list = Account.objects.all()
    for account in account_list:
        account.clean_cache()
