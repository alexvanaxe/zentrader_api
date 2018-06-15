from django.db import models

from django.utils.translation import ugettext_lazy as _


class Stock(models.Model):
    code = models.CharField(_('Code'), max_length=5)
    price = models.DecimalField(_('stock value'), max_digits=22, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return self.code
