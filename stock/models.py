from decimal import Decimal
from datetime import datetime
from django.db import models

from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from operation.models import Operation
from account.models import Account
from formulas import support_system_formulas

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
        sells = Operation.objects.filter(stock=self).aggregate(Sum('selldata__amount'))['selldata__amount__sum'] or Decimal(0)

        buys = Operation.objects.filter(stock=self).aggregate(Sum('buydata__amount'))['buydata__amount__sum'] or Decimal(0)

        return  buys - sells


    def average_price(self, date__gte=None, date__lte=datetime.now()):
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
        operations = Operation.objects.filter(stock=self).order_by('date')

        if date__gte:
            operations = operations .filter(date__gte=date__gte)

        if date__lte:
            operations = operations .filter(date__lt=date__lte)

        actual_average_price = Decimal('0')
        net_amount = Decimal('0')

        for operation in operations:
            if operation.kind() == Operation.Kind.BUY:
                operation_average_price = support_system_formulas.calculate_average_price(operation.amount,
                                                                operation.price,
                                                                operation.account.operation_cost)

                actual_average_price = ((actual_average_price * net_amount) + (operation_average_price * operation.amount))/(net_amount + operation.amount)
                net_amount += operation.amount
            if operation.kind() == Operation.Kind.SELL:
                net_amount = net_amount - operation.amount

        return actual_average_price
