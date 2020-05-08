from django.db import models

from django.utils.translation import ugettext_lazy as _
from decimal import Decimal

from operation.models import Operation
from account.models import Account
from formulas import support_system_formulas


class ExperienceData(Operation):
    """ Some additional data and functions specifics for the experiments """
    BUY = 'B'
    SELL = 'S'

    INTENTION = (
        (BUY, 'Buy'),
        (SELL, 'Sell')
    )

    def __str__(self):
        return str(self.stock.code) + " " + str(self.creation_date)

    target = models.DecimalField(_('target price'), max_digits=22, decimal_places=2, null=True, blank=True)
    stop_gain = models.DecimalField(_('stop gain'), max_digits=22, decimal_places=2, null=True, blank=True)
    stop_loss = models.DecimalField(_('stop loss'), max_digits=22, decimal_places=2, null=True, blank=True)
    limit = models.DecimalField(_('limit'), max_digits=6, decimal_places=2, null=True, blank=True)
    action = models.TextField(_('action'), null=True, blank=True, max_length=140)
    intent = models.CharField(max_length=1, null=True, blank=True, choices=INTENTION, default=BUY)

    def kind(self):
        self.kind_buffer = self.Kind.EXPERIMENT
        return self.kind_buffer

    def buy_set(self):
        return self.buydata_set.filter(archived=False)

    def experience_gain(self):
        """
        Return how would be the gain if the sell price of the operation was now.

        We consider that the price is the price bought and the sell is the actual stock value
        """
        return self.calculate_gain(self.stock.price)

    def experience_gain_percent(self):
        return self.calculate_gain_percent(self.stock.price)

    def experience_total_gain_percent(self):
        gain = self.experience_gain()
        return Decimal(support_system_formulas.calculate_percentage(gain, self.account.total_equity()))

    def target_gain(self):
        """
        Calculate the gain based in the stock value.

        Make use of the internal _calculate_gain of the operation.


        :returns: The gain
        :rtype: Decimal

        """
        if self.target:
            return self.calculate_gain(self.target)

    def target_gain_total_percent(self):
        target_value = self.target_gain()

        if target_value:
            return Decimal(support_system_formulas.calculate_percentage(target_value, self.account.total_equity()))

    def target_gain_percent(self):
        """
        Calculate the percentage of the target that we will gain

        :returns: The Percentage of the target gain
        :rtype: Decimal
        """
        # Same as in the buy, hava to inicialize the decimals
        return self.calculate_gain_percent(self.target)

    def stop_loss_result(self):
        """
        Calculate the operation result case the stop is hit.
        """
        if self.stop_loss:
            return self.calculate_gain(self.stop_loss)

    def stop_loss_total_percent(self):
        stop_loss_result = self.stop_loss_result()
        if stop_loss_result:
            return Decimal(support_system_formulas.calculate_percentage(stop_loss_result,
                           self.account.total_equity()))

    def stop_loss_percent(self):
        """
        Calculates the percentage result of the stop loss if it is hit.
        """
        if self.stop_loss:
            return self.calculate_gain_percent(self.stop_loss)

    def operation_limit(self):
        """
        Calculates the limit acceptable to make a buy.

         The idea is to first define a stop, then we can get how much is the value of the stock will represent the percentage
          limitation of the piranha.
         For instance: if the amount is 500 and the stop loss is 8, then I can buy the stock until the value of 8.58, any
          value further this will violate the piranha rule.

        :returns: The limit
        :rtype: Decimal

        """
        if not self.stop_loss:
            return None

        account = self.account
        return Decimal(support_system_formulas.calculate_limit(support_system_formulas.PIRANHA_LIMIT,
                                                               account.total_equity(),
                                                               self.operation_cost(),
                                                               self.stop_loss,
                                                               self.amount))

    def intents(self):
        return self.INTENTION
