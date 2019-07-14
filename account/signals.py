from django.db.models.signals import post_save
from django.dispatch import receiver

from sell.models import SellData
from buy.models import BuyData
from stock.models import Stock
from account.models import Account


@receiver(post_save, sender=BuyData)
def debit_account(sender, instance, created, **kwargs):
    if (kwargs.get('created', True) and not kwargs.get('raw', False)):
        if created:
            account = instance.account
            account.equity = account.equity - instance.average_cost()
            account.save()
            account_list = Account.objects.all()
            for account in account_list:
                account.clean_cache()


@receiver(post_save, sender=SellData)
def credit_account(sender, instance, created, **kwargs):
    if (kwargs.get('created', True) and not kwargs.get('raw', False)):
        if instance.executed:
            account = instance.account
            account.equity = account.equity + instance.sell_value()
            account.save()
            account_list = Account.objects.all()
            for account in account_list:
                account.clean_cache()


@receiver(post_save, sender=Stock)
def update_total_equity_cache(sender, instance, created, **kwargs):
    if (kwargs.get('created', True) and not kwargs.get('raw', False)):
        account_list = Account.objects.all()
        for account in account_list:
            account.clean_cache()
