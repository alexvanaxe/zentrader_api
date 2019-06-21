from django.db.models.signals import post_save
from django.dispatch import receiver

from sell.models import SellData
from buy.models import BuyData


@receiver(post_save, sender=BuyData)
def update_stocks_on_buy(sender, instance, created, **kwargs):
    if created:
        instance.stock.clean_cache()


@receiver(post_save, sender=SellData)
def update_stocks_on_sell(sender, instance, created, **kwargs):
    if instance.executed:
        instance.stock.clean_cache()
