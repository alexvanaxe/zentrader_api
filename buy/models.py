from django.db import models

from decimal import Decimal
from django.core.exceptions import ValidationError

from operation.models import Operation
from formulas import support_system_formulas

class BuyData(Operation):
    experience = models.ForeignKey('experience.ExperienceData', null=True, on_delete=models.CASCADE)
    amount_available_b = None

    def __str__(self):
        return str(self.stock.code) + " " + str(self.creation_date)

    def sell_set(self):
        return self.selldata_set.filter(archived=False)

    def amount_available(self, executed_filter=None):
        """
        Return the amount available to sell
        The default returns all even the archived.
        The executed_filter can be sended, so in the sells we consider accordinly if it is
        false or true.
        """
        if self.amount_available_b is not None:
            return self.amount_available_b

        if executed_filter is not None:
            self.amount_available_b = self.amount - (self.selldata_set.filter(executed=executed_filter).aggregate(models.Sum('amount'))['amount__sum'] or Decimal(0))
            return self.amount_available_b

        else:
            self.amount_available_b = self.amount - ((self.selldata_set.filter(archived=False).aggregate(models.Sum('amount'))['amount__sum'] or Decimal(0)) + (self.selldata_set.filter(executed=True, archived=True).aggregate(models.Sum('amount'))['amount__sum'] or Decimal(0)))
            return self.amount_available_b

    def operation_gain(self):
        """
        Calculate the gain based in the stock value.

        Make use of the internal _calculate_gain of the operation.


        :returns: The gain
        :rtype: Decimal

        """
        return self.calculate_gain(self.stock.price)

    def operation_gain_percent(self):
        """
        Calculate the percentage gain, considering that the stock would be sold
        by the current stock value.

        :returns: The percentage gain
        :rtype: Decimal
        """
        # This should be returned as decimal, but it is not, so we convert it
        # here
        return Decimal(support_system_formulas.calculate_gain_percent(
            Decimal(self.stock.price),
            Decimal(self.price),
            Decimal(self.amount),
            Decimal(self.operation_cost())))

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)

        if self.cost() > self.account.equity:
            raise ValidationError('Not enough money to make this transaction')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def remaining_gain(self):
        amount_available = self.amount_available(executed_filter=True)
        if amount_available > 0:
            return Decimal(support_system_formulas.calculate_sell(Decimal(amount_available), Decimal(self.stock.price), self.operation_cost(self.Kind.SELL)))
        else:
            return Decimal(0)
