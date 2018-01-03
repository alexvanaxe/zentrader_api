from decimal import Decimal
from django.core.validators import MinValueValidator

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Account(models.Model):
    """
    An account with a broker.

    The total money there is in a broker is the equity plus the gain.

    Fields:

    * broker -- The name of the broker. (ex: banifast)
    * operation_cost -- The cost of the operation without the taxes applied.
    * equity -- The money that I put from my pocket in the broker.

    """
    def __unicode__(self):
        return self.broker

    broker = models.CharField(_('broker'), null=False, unique=True, max_length=120)
    operation_cost = models.DecimalField(_('operation cost'), max_digits=7, decimal_places=2, null=False)
    equity = models.DecimalField(_('equity'), max_digits=15, decimal_places=2, null=False)