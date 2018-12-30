from django.db import models
from datetime import datetime
from decimal import Decimal, ROUND_DOWN

from django.utils.translation import ugettext_lazy as _

import account.models as account

class PaperOperation(models.Model):
    """ A paper operation realized in a transaction (ex: buy, sell, experiment...).
    The paper operation is an operation that is not real, not made in the stocks.
    It is just to learing proposes."""

    FAVORITE = (
        ('Y', _('Yes')),
        ('N', _('No'))
    )

    def __str__(self):
        return str(self.pk)

    account = models.ForeignKey('account.Account', on_delete=models.CASCADE)
    stock = models.ForeignKey('stock.Stock', on_delete=models.CASCADE)
    creation_date = models.DateTimeField(_('creation date'), null=False, editable=False)
    amount = models.DecimalField(_('amount'), max_digits=22, decimal_places=0, null=False, blank=False)
    price = models.DecimalField(_('price'), max_digits=22, decimal_places=2, null=False, blank=False)
    archived = models.BooleanField(_('archived'), default=False)
    nickname = models.TextField(_('nickname'), null=True, blank=True, max_length=100)

    def save(self, *args, **kwargs):
        """
        It overrides the django models save.

        On save, we update the timestamp of the creation date. It is only updated if there isn't a value defined.
          So it will not be changed on updates.

        """
        try:
            self.account
        except account.Account.DoesNotExist:
            self.account = account.Account.objects.all().order_by('-pk')[0]

        if not self.creation_date:
            self.creation_date = datetime.now()

        super().save(*args, **kwargs)


class PaperBuy(PaperOperation):
    """
    A Paper buy is a fake buy just for learning purposes.
    """
    experience = models.ForeignKey('operation.ExperienceData', null=True,
                                   on_delete=models.CASCADE)

    def __str__(self):
        return str(self.stock.code) + " " + str(self.creation_date)

    def stock_data(self):
        """
        Returns the stock data
        """
        return self.stock


class PaperSell(PaperOperation):
    """
    A paper sell is just a fake sell for learning purposes.
    """
    paper_buy = models.ForeignKey('learning.PaperBuy', null=True,
                                  on_delete=models.CASCADE)
    stop_gain = models.DecimalField(_('stop gain'), max_digits=22,
                                    decimal_places=2, null=True, blank=True)
    stop_loss = models.DecimalField(_('stop loss'), max_digits=22,
                                    decimal_places=2, null=True, blank=True)

    def __str__(self):
        return str(self.stock.code) + " " + str(self.creation_date)
