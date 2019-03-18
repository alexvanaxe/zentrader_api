from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.core.cache import cache


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

    def update_total_equity(self):
        """
        Update the cache for the total_equity
        """
        operations = self.operation_set.filter(buydata__isnull=False).select_related('buydata')
        total_equity = (sum(i.buydata.remaining_gain() for i in operations)) + self.equity
        cache.set('total_equity_%d' % self.pk, total_equity)
        return total_equity

    def clean_cache(self):
        """
        Clean the cache when the value need be updated
        """
        cache.delete('total_equity_%d' % self.pk)

    def total_equity(self):
        """
        Returns the total equity. This is a cached value, set for 1 day long.
        """
        total_equity = cache.get('total_equity_%d' % self.pk)
        if total_equity is None:
            operations = self.operation_set.filter(buydata__isnull=False).select_related('buydata')
            total_equity = (sum(i.buydata.remaining_gain() for i in operations)) + self.equity
            cache.set(('total_equity_%d' % self.pk), total_equity)

        return total_equity

def default_account():
    return Account.objects.filter(next_account__isnull=True)[0]
