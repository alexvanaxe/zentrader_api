from django.db import models
from django.utils.translation import ugettext_lazy as _

import operation


class Account(models.Model):
    """
    An account with a broker.

    The total money there is in a broker is the equity plus the gain.

    Fields:

    * broker -- The name of the broker. (ex: banifast)
    * operation_cost -- The cost of the operation without the taxes applied.
    * equity -- The money that I put from my pocket in the broker.

    """
    def __str__(self):
        return self.broker

    next_account = models.ForeignKey('account.Account',
                                     on_delete=models.CASCADE, null=True,
                                     blank=True)
    broker = models.CharField(_('broker'), null=False, max_length=120)

    operation_cost_day_trade = models.DecimalField(_('Cost Day Trade'),
                                                   max_digits=7,
                                                   decimal_places=2, null=False)
    operation_cost_fraction = models.DecimalField(_('Cost Fraction'),
                                                  max_digits=7,
                                                  decimal_places=2, null=False)
    operation_cost_position = models.DecimalField(_('Cost Normal'),
                                                  max_digits=7,
                                                  decimal_places=2, null=False)
    equity = models.DecimalField(_('equity'), max_digits=15, decimal_places=2,
                                 null=False)


    def total_equity(self):
        return (sum(i.buydata.remaining_gain() for i in self.operation_set.filter(buydata__isnull=False))) + self.equity


def default_account():
    return Account.objects.filter(next_account__isnull=True)[0]
