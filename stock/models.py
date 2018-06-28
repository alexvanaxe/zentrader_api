from decimal import Decimal
from django.db import models

from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from operation.models import Operation

class Stock(models.Model):
    code = models.CharField(_('Code'), max_length=5)
    price = models.DecimalField(_('stock value'), max_digits=22, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return self.code

    def owned(self):
        """
        Quantify the amount of stock that is owned at the moment (it is the
        quantity available to sell).

        :returns: The amount owned
        :rtype: Decimal
        """
        sells = Operation.objects.filter(stock=self).aggregate(Sum('selldata__amount'))['selldata__amount__sum']

        buys = Operation.objects.filter(stock=self).aggregate(Sum('buydata__amount'))['buydata__amount__sum']

        if sells is not None and buys is not None:
            return  buys - sells
        else:
            return Decimal(0)
