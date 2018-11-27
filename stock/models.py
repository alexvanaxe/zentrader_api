from decimal import Decimal
from datetime import datetime
from django.db import models

from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from operation.models import Operation
from account.models import Account
from formulas import support_system_formulas


class Stock(models.Model):
    code = models.CharField(_('Code'), max_length=10)
    name = models.CharField(_('Name'), max_length=140)
    sector = models.CharField(_('Sector'), null=True, blank=True, max_length=140)
    subsector = models.CharField(_('Subsector'), null=True, blank=True, max_length=140)
    price = models.DecimalField(_('stock value'), max_digits=22, decimal_places=2, null=False, blank=False)

    def __str__(self):
        return self.code

    def owned(self, date__gte=None, date__lte=None):
        """
        Quantify the amount of stock that is owned at the moment (it is the
        quantity available to sell).

        :returns: The amount owned
        :rtype: Decimal
        """

        if date__lte is None:
            date__lte = datetime.now()

        sells_q = Operation.executions.filter(stock=self)
        buys_q = Operation.objects.filter(stock=self)
        if date__gte:
            sells_q = sells_q.filter(creation_date__gte=date__gte)
            buys_q = buys_q.filter(creation_date__gte=date__gte)
        if date__lte:
           sells_q =  sells_q.filter(creation_date__lte=date__lte)
           buys_q = buys_q.filter(creation_date__lte=date__lte)

        sells = sells_q.aggregate(Sum('selldata__amount'))['selldata__amount__sum'] or Decimal(0)
        buys = buys_q.aggregate(Sum('buydata__amount'))['buydata__amount__sum'] or Decimal(0)

        return  buys - sells


    def average_price(self, date__gte=None, date__lte=None):
        """
        The average price of the stock is a concept used in the calculations of the brazilian ir.
        The main reason of the existence of this value is the fact that we can't choose the action we will sell. So
        it is difficult to define the result (balance) of the operation. To solve the problem it is used the concept
        of average price. Which is a single mathematical average.

        More information can be found in the `Bussola
        <http://blog.bussoladoinvestidor.com.br/calculo-do-preco-medio-de-acoes/>`_.


        :param reference_date: The date to cut until when the operations will be considered.

        :returns: The average price
        :rtype: Decimal
        """
        if date__lte is None:
            date__lte = datetime.now()

        operations = Operation.objects.filter(stock=self).order_by('creation_date')

        if date__gte:
            operations = operations .filter(creation_date__gte=date__gte)

        if date__lte:
            operations = operations .filter(creation_date__lte=date__lte)

        actual_average_price = Decimal('0')
        net_amount = Decimal('0')

        for operation in operations:
            if operation.kind() == Operation.Kind.BUY:
                operation_average_price = support_system_formulas.calculate_average_price(operation.amount,
                                                                operation.price,
                                                                operation.operation_cost())

                actual_average_price = ((actual_average_price * net_amount) + (operation_average_price * operation.amount))/(net_amount + operation.amount)

                net_amount += operation.amount
            if operation.kind() == Operation.Kind.SELL:
                net_amount = net_amount - operation.amount


        return Decimal(actual_average_price)

    def stock_value(self):
        return Decimal(self.owned()) * Decimal(self.average_price())

    def stock_result(self):
        """Returns the result of the stock. It is considered as operation cost
        the wrost case scenario, that is of the position.
        TODO: The way it is used in the system now it is garanteed that it has
        some owned and some average price. But in the future errors might
        occur.
        :returns: Decimal
        """
        operation_cost = Account.objects.filter(next_account__isnull=True)[0]

        return Decimal(support_system_formulas.calculate_gain(self.price,
                                                              self.average_price(),
                                                              self.owned(),
                                                              operation_cost.operation_cost_position))

    def stock_result_percent(self):
        """ This has the same logic that stock_result, and returns the
        variation from the actual stock price.
        :returns: TODO
        """
        operation_cost = Account.objects.filter(next_account__isnull=True)[0]

        return Decimal(support_system_formulas.calculate_gain_percent(
            self.price, self.average_price(), self.owned(), operation_cost.operation_cost_position))
