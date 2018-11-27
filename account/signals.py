from django.db.models.signals import post_save
from django.dispatch import receiver

from operation.models import BuyData, SellData
from account.models import Account

@receiver(post_save, sender=BuyData)
def debit_account(sender, instance, created, **kwargs):
    if created:
       account = instance.account
       account.equity = account.equity - instance.average_cost()
       account.save()

@receiver(post_save, sender=SellData)
def credit_account(sender, instance, created, **kwargs):
    if instance.executed:
       account = instance.account
       account.equity = account.equity + instance.sell_value()
       account.save()
