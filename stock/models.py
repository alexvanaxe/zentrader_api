from decimal import Decimal
from datetime import datetime
from django.db import models
from django.core.cache import cache

from django.db.models import Sum, Q
from django.utils.translation import ugettext_lazy as _
from operation.models import Operation, BuyData
from account.models import Account, default_account
from formulas import support_system_formulas


class StockResume():
    def __init__(self, code, name, sector, subsector, price, owned, average_available_price,
                 stock_value, stock_result, stock_result_percent, stock_result_total_percent, owner):
        self.code = code
        self.name = name
        self.sector = sector
        self.subsector = subsector
        self.price = price
        self.owned = owned
        self.average_available_price = average_available_price
        self.stock_value = stock_value
        self.stock_result = stock_result
        self.stock_result_percent = stock_result_percent
        self.stock_result_total_percent = stock_result_total_percent
        self.owner = owner


class StockResumeManager(models.Manager):
    def get_resume(self, stock):
        stock_resume = StockResume(stock.code, stock.name, stock.sector,
                                    stock.subsector, stock.price, stock.owned(),
                                    stock.average_available_price, stock.stock_value,
                                    stock.stock_result, stock.stock_result_percent,
                                    stock.stock_result_total_percent,
                                    owner='')
        return stock_resume

    def all(self):
        stocks = self.select_related()
        stocks_resumes = []
        for stock in stocks:
            owned = stock.owned()
            if owned > 0:
                stock_resume = StockResume(stock.code, stock.name, stock.sector, stock.subsector,
                                           stock.price, owned, stock.average_available_price,
                                           stock.stock_value, stock.stock_result,
                                           stock.stock_result_percent, stock.stock_result_total_percent, owner='')

                stocks_resumes.append(stock_resume)

        return stocks_resumes

    def filter(self, owner):
        stocks = self.select_related()
        stocks_resumes = []
        for stock in stocks:
            owned = stock.owned(owner=owner)
            if owned > 0:
                stock_resume = StockResume(stock.code, stock.name, stock.sector,
                                           stock.subsector, stock.price, owned,
                                           stock.average_available_price(owner=owner),
                                           stock.stock_value(owner=owner),
                                           stock.stock_result(owner=owner),
                                           stock.stock_result_percent(owner=owner),
                                           stock.stock_result_total_percent(owner=owner),
                                           owner=owner.username)

                stocks_resumes.append(stock_resume)

        return stocks_resumes


class Stock(models.Model):
    code = models.CharField(_('Code'), max_length=10)
    name = models.CharField(_('Name'), max_length=140)
    sector = models.CharField(_('Sector'), null=True, blank=True, max_length=140)
    subsector = models.CharField(_('Subsector'), null=True, blank=True, max_length=140)
    price = models.DecimalField(_('stock value'), max_digits=22, decimal_places=2,
                                null=False, blank=False)

    objects = models.Manager()
    resume = StockResumeManager()


    def __str__(self):
        return self.code

    def clean_cache(self):
        cache.delete(self.code + 'owned')
        cache.delete(self.code + 'average_price')

    def update_owned_cache(self):
        date__lte = datetime.now()

        sells_q = Operation.executions.filter(stock=self).select_related('selldata')
        buys_q = Operation.executions.filter(stock=self).select_related('buydata')

        if date__lte:
            sells_q = sells_q.filter(creation_date__lte=date__lte)
            buys_q = buys_q.filter(creation_date__lte=date__lte)

        sells = sells_q.aggregate(Sum('selldata__amount'))['selldata__amount__sum'] or Decimal(0)
        buys = buys_q.aggregate(Sum('buydata__amount'))['buydata__amount__sum'] or Decimal(0)
        owned_stocks = buys - sells
        cache.set(self.code + 'owned', owned_stocks)
        return owned_stocks

    def owned(self, date__gte=None, date__lte=None, owner=None):
        use_cache = False
        if date__gte is None and date__lte is None and owner is None:
            use_cache = True
            owned_stocks = cache.get(self.code + 'owned')
            if owned_stocks is not None:
                return owned_stocks

        if owner is not None:
            owned_stocks = self._owned(Operation.executions.filter(owner=owner),
                                       date__gte=date__gte, date__lte=date__lte)
        else:
            owned_stocks = self._owned(Operation.executions.all(),
                                       date__gte=date__gte, date__lte=date__lte)

        if use_cache:
            cache.set(self.code + 'owned', owned_stocks)

        return owned_stocks


    def _owned(self, queryset, date__gte=None, date__lte=None):
        """
        Quantify the amount of stock that is owned at the moment (it is the
        quantity available to sell).

        :returns: The amount owned
        :rtype: Decimal
        """
        if date__lte is None:
            date__lte = datetime.now()

        sells_q = queryset.filter(stock=self).select_related('selldata')
        buys_q = queryset.filter(stock=self).select_related('buydata')
        if date__gte:
            sells_q = sells_q.filter(creation_date__gte=date__gte)
            buys_q = buys_q.filter(creation_date__gte=date__gte)
        if date__lte:
            sells_q = sells_q.filter(creation_date__lte=date__lte)
            buys_q = buys_q.filter(creation_date__lte=date__lte)

        sells = sells_q.aggregate(Sum('selldata__amount'))['selldata__amount__sum'] or Decimal(0)
        buys = buys_q.aggregate(Sum('buydata__amount'))['buydata__amount__sum'] or Decimal(0)

        owned_stocks = buys - sells

        return owned_stocks

    def average_price(self, date__gte=None, date__lte=None, owner=None):
        """
        The average price of the stock is a concept used in the calculations of the brazilian ir.
        The main reason of the existence of this value is the fact that we can't choose the action we will sell. So
        it is difficult to define the result (balance) of the operation. To solve the problem it is used the concept
        of average price. Which is a single mathematical average.

        There is no issue here to use the category straight because it uses only the executed operations
        to perform the calculations.

        ATTENTION: It is a very expensive operation
        This value is being cached when the default value is passed

        More information can be found in the `Bussola
        <http://blog.bussoladoinvestidor.com.br/calculo-do-preco-medio-de-acoes/>`_.


        :param reference_date: The date to cut until when the operations will be considered.

        :returns: The average price
        :rtype: Decimal
        """
        def _get_operations_queryset(owner):
            if owner is None:
                operations = (
                    Operation.executions.filter(stock=self).order_by('execution_date')
                    .select_related('buydata', 'selldata', 'account'))

                return operations
            else:
                operations = (
                    Operation.executions.filter(stock=self).filter(owner=owner).
                    order_by('execution_date').select_related('buydata', 'selldata',
                                                              'account'))

                return operations

        use_cache = False
        if date__lte is None and date__gte is None and owner is not None:
            use_cache = True

        if use_cache:
            average_price = cache.get(self.code + 'average_price')
            if average_price is not None:
                return average_price

        if date__lte is None:
            date__lte = datetime.now()

        operations = _get_operations_queryset(owner)

        if date__gte:
            operations = operations.filter(creation_date__gte=date__gte)

        if date__lte:
            operations = operations.filter(creation_date__lte=date__lte)

        actual_average_price = Decimal('0')
        net_amount = Decimal('0')

        operations = operations.filter(experiencedata__isnull=True)
        for operation in operations:

            if operation.kind() == Operation.Kind.BUY:
                operation_average_price = support_system_formulas.calculate_average_price(operation.amount,
                                                                operation.price,
                                                                operation.operation_cost())

                actual_average_price = ((actual_average_price * net_amount) +
                                        (operation_average_price * operation.amount))/(net_amount + operation.amount)

                net_amount += operation.amount
            if operation.kind() == Operation.Kind.SELL:
                net_amount = net_amount - operation.amount

        if use_cache:
            cache.set(self.code + 'average_price', actual_average_price)

        return Decimal(actual_average_price)

    def average_available_price(self, owner=None):
        """
        The open price is an average price evolued. It is considered all the open positions we have
        in the stock to calculate how much the price is for the stock.
        Unfortunely we aren't able to replace the average stock with this, because the average
        stock is the current form used in the brazilian ir.
        """
        def _get_buys_queryset(owner):
            if owner is None:
                buys = BuyData.objects.filter(Q(selldata__executed=False) | Q(selldata__isnull=True), stock=self).order_by('execution_date')
                return buys
            else:
                buys = BuyData.objects.filter(Q(selldata__executed=False) | Q(selldata__isnull=True), stock=self, owner=owner).order_by('execution_date')
                return buys

        actual_average_price = Decimal('0')
        net_amount = Decimal('0')

        buys = _get_buys_queryset(owner)

        for buy in buys:
            amount_available = buy.amount_available(executed_filter=True)
            operation_average_price = (support_system_formulas.calculate_average_price(amount_available,
                                       buy.price,
                                       buy.operation_cost()))

            actual_average_price = ((actual_average_price * net_amount) +
                                    (operation_average_price * amount_available))/(net_amount + amount_available)

            net_amount += amount_available

        return Decimal(actual_average_price)

    def stock_value(self, owner=None):
        """
        Returns the Stock value, ie: How much is owned now multipled by the current price.
        PS: It can be made an improvement to calculate the average price using only the owned.
        """
        return Decimal(self.owned(owner=owner)) * Decimal(self.price)

    def stock_sell_price(self, owner=None):
        owned = self.owned(owner=owner)
        if owned > 0:
            return Decimal(support_system_formulas.calculate_sell(owned,
                                                                  self.price,
                                                                  default_account()
                                                                  .operation_cost_position))
        else:
            return 0

    def stock_result(self, owner=None):
        """Returns the result of the stock. It is considered as operation cost
        the wrost case scenario, that is of the position.
        TODO: The way it is used in the system now it is garanteed that it has
        some owned and some average price. But in the future errors might
        occur.
        :returns: Decimal
        """
        operation_cost = Account.objects.filter(next_account__isnull=True)[0]

        return Decimal(support_system_formulas.calculate_gain(self.price,
                                                              self.average_price(owner=owner),
                                                              self.owned(owner=owner),
                                                              operation_cost.operation_cost_position))

    def stock_result_percent(self, owner=None):
        """ This has the same logic that stock_result, and returns the
        variation from the actual stock price.
        :returns: TODO
        """
        operation_cost = Account.objects.filter(next_account__isnull=True)[0]

        return Decimal(support_system_formulas.calculate_gain_percent(
            self.price, self.average_price(owner=owner), self.owned(owner=owner),
            operation_cost.operation_cost_position))

    def stock_result_total_percent(self, owner=None):
        stock_result = self.stock_result(owner=owner)

        if stock_result:
            return Decimal(support_system_formulas.calculate_percentage(stock_result,
                                                                        default_account().total_equity()))
