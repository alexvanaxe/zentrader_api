from datetime import datetime

from decimal import Decimal
from django.db import models

from django.utils.translation import ugettext_lazy as _

from operation.models import Operation
from formulas import support_system_formulas


class RiskData(object):
    def __init__(self, shark):
        self.shark = shark

class SellDataManager(models.Manager):
    def shark(self):
        sells = SellData.objects.filter(archived=False).filter(executed=False)
        shark = 0

        for sell in sells:
            stop_loss = 0
            if sell.stop_loss:
               stop_loss = sell.stop_loss
            gain_percent = sell.calculate_gain(stop_loss, sell.buy.price)
            if gain_percent < 0:
                shark = (support_system_formulas.calculate_percentage(gain_percent, sell.account.total_equity()) * -1) + shark

        risk_data = RiskData(round(shark, 2))
        return risk_data


class SellData(Operation):
    buy = models.ForeignKey('buy.BuyData', null=True, on_delete=models.CASCADE)
    stop_gain = models.DecimalField(_('stop gain'), max_digits=22, decimal_places=2, null=True, blank=True)
    stop_loss = models.DecimalField(_('stop loss'), max_digits=22, decimal_places=2, null=True, blank=True)

    solds = SellDataManager()

    def kind(self):
        self.kind_buffer = self.Kind.SELL
        return self.kind_buffer


    def __str__(self):
        return str(self.stock.code) + " " + str(self.creation_date)

    def _getLteDate(self):
        if self.executed:
            return self.execution_date
        else:
            return None

    def amount_available(self, executed_filter=None):
        if self.buy:
            return self.buy.amount_available(executed_filter)
        else:
            return Decimal(0)

    def result(self, sell_price=None):
        """ Return the result to be used in the ir operation. It is a very expensive operation, and is worthless to be cached
            because it is date dependent, and operation dependent.
        """
        if not sell_price:
            sell_price = self.price

        if not self.operation_category() == 'DT':
                return Decimal(support_system_formulas.calculate_average_gain(sell_price, self.stock.average_price(date__lte=self._getLteDate()), self.operation_cost(), self.amount))

        return Decimal(support_system_formulas.calculate_average_gain(sell_price, self.stock.average_price(date__lte=datetime.strptime('%d-%d-%d:23:59' % (self.creation_date.year, self.creation_date.month, self.creation_date.day), '%Y-%m-%d:%H:%M'), date__gte=datetime.strptime('%d-%d-%d' % (self.creation_date.year, self.creation_date.month, self.creation_date.day), '%Y-%m-%d')), self.operation_cost(), self.amount))

    def gain_percent(self):
        if not self.is_daytrade():
            return Decimal(support_system_formulas.calculate_gain_percent(self.price, self.stock.average_price(date__lte=self._getLteDate()), self.amount, self.operation_cost()))
        else:
            return Decimal(support_system_formulas.calculate_gain_percent(self.price, self.stock.average_price(date__lte=datetime.strptime('%d-%d-%d:23:59' % (self.creation_date.year, self.creation_date.month, self.creation_date.day), '%Y-%m-%d:%H:%M'), date__gte=datetime.strptime('%d-%d-%d' % (self.creation_date.year, self.creation_date.month, self.creation_date.day), '%Y-%m-%d')), self.amount, self.operation_cost()))

    def stock_profit(self):
        """
        Return the result of the stock based on the stock price
        """
        if self.buy is not None:
            return self.calculate_gain(self.stock.price, self.buy.price)
        else:
            return 0

    def stock_profit_total_percent(self):
        """ Returns the total percent result of the stock, based on the total
        equity.
        :returns: Decimal with the total percent

        """
        stock_profit = self.stock_profit

        if stock_profit:
            return Decimal(support_system_formulas.calculate_percentage(stock_profit(),
                                                                        self.account.total_equity()))

    def stock_profit_percent(self):
        """
        Return the profit percent result based on the stock price
        """
        if self.buy is not None:
            return self.calculate_gain_percent(self.stock.price, self.buy.price)
        else:
            return 0

    def profit(self):
        """
        Return the result of the stock based on the bought price only
        """
        if self.buy is not None:
            return self.calculate_gain(self.price, self.buy.price)
        else:
            return 0

    def profit_percent(self):
        """
        Return the profit percent result based on the bought price only
        """
        if self.buy is not None:
            return self.calculate_gain_percent(self.price, self.buy.price)
        else:
            return 0

    def profit_total_percent(self):
        """ Returns the percent of the profit of this operation based on the total
        equity.
        :returns: Deciamal with the percentage

        """
        profit = self.profit()

        if profit:
            return Decimal(support_system_formulas.calculate_percentage(profit,
                                                                        self.account.total_equity()))

    def sell_value(self):
        """
        Returns how much money will be aquired with the sell
        """
        return Decimal(support_system_formulas.calculate_sell(self.amount, self.price, self.operation_cost()))

    def stop_gain_result(self):
        """
        Calculate the operation result case the stop is hit.
        """
        stop_gain = 0
        if self.stop_gain:
            stop_gain = self.stop_gain

        if self.buy is None:
            return -99999

        return self.calculate_gain(stop_gain, self.buy.price)

    def stop_gain_percent(self):
        """
        Calculates the percentage result of the stop gain if it is hit.
        """
        stop_gain = 0
        if self.stop_gain:
            stop_gain = self.stop_gain

        if self.buy is None:
            return -99999

        return self.calculate_gain_percent(stop_gain, self.buy.price)

    def stop_loss_result(self):
        """
        Calculate the operation result case the stop is hit.
        """
        stop_loss = 0
        if self.stop_loss:
            stop_loss = self.stop_loss

        if self.buy is None:
            return -99999

        return self.calculate_gain(stop_loss, self.buy.price)

    def stop_loss_total_percent(self):
        """ Returns the percentage of the stop loss based on the total equity
        (equity + stocks owned)

        :returns: Decimal with total percent

        """
        stop_loss = self.stop_loss_result()

        if stop_loss:
            return Decimal(support_system_formulas.calculate_percentage(stop_loss,
                           self.account.total_equity()))

    def stop_loss_percent(self):
        """
        Calculates the percentage result of the stop loss if it is hit.
        """
        stop_loss = 0
        if self.stop_loss:
            stop_loss = self.stop_loss

        if self.buy is None:
            return -99999

        return self.calculate_gain_percent(stop_loss, self.buy.price)

    def buy_price(self):
        """
        Return the price of the buy associated with this sell
        """
        return self.buy.price
