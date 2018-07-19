from django.db.models.signals import post_save
from django.dispatch import receiver

from operation.models import BuyData, SellData
from account.models import Account

@receiver(post_save, sender=BuyData)
def debit_account(sender, instance, created, **kwargs):
    if created:
       instance.account.equity = instance.account.equity - instance.average_cost()
       instance.save()

@receiver(post_save, sender=SellData)
def credit_account(sender, instance, created, **kwargs):
    if created:
       instance.account.equity = instance.account.equity + instance.calculate_gain()
       instance.save()

