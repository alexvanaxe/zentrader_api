from datetime import datetime
from enum import Enum
import pytz

from decimal import Decimal, ROUND_DOWN
from django.db import models

from django.utils.translation import ugettext_lazy as _

from account.models import Account
from trade_system.models import Analysis
from formulas import support_system_formulas

# def get_image_path(instance, filename):
#     """ Get the path where the images are stored in the filesystem """
#     return os.path.join('charts', str(instance.transaction.id), instance.operation_status.name,
#                         str(time.mktime(instance.creation_date.timetuple())), filename)

class OperationManager(models.Manager):

    """ A manager for the operation. It is used to provide a shortcut for the
    operations that were executed. """
    def get_queryset(self):
        return super().get_queryset().filter(executed=True)


class Operation(models.Model):
    """ A operation realized in a transaction (ex: buy, sell, experiment...) """

    FAVORITE = (
        ('Y', _('Yes')),
        ('N', _('No'))
    )

    CATEGORY = (
        ('DT', _('Daytrade')),
        ('O', _('Ordinary')),
        ('F', _('Fraction')),
        ('NA', _('Not yet Defined'))
    )

    def __str__(self):
        return str(self.pk)

    owner = models.ForeignKey('auth.User', related_name='operations',
                              on_delete=models.CASCADE)
    account = models.ForeignKey('account.Account', on_delete=models.CASCADE)
    stock = models.ForeignKey('stock.Stock', on_delete=models.CASCADE)
    analysis = models.OneToOneField('trade_system.Analysis', null=True,
                                    on_delete=models.CASCADE)
    creation_date = models.DateTimeField(_('creation date'), null=False,
                                         editable=False)
    execution_date = models.DateTimeField(_('execution date'), null=True,
                                          blank=True)
    amount = models.DecimalField(_('amount'), max_digits=22, decimal_places=0,
                                 null=False, blank=False)
    price = models.DecimalField(_('stock value'), max_digits=22,
                                decimal_places=2, null=False, blank=False)
    category = models.CharField(max_length=2, choices=CATEGORY, default='NA',
                                null=False, blank=False)
    archived = models.BooleanField(_('archived'), default=False)
    executed = models.BooleanField(_('executed'), default=False)
    nickname = models.TextField(_('nickname'), null=True, blank=True,
                                max_length=100)

    favorite = models.IntegerField(_('favorite'), default=0)

    # DEFINE THE MANAGERS
    objects = models.Manager()  # The default manager
    executions = OperationManager()  # The executed manager

    dt_result = None
    kind_buffer = None

#    chart = models.ImageField(_('chart graph'), null=True, blank=True, upload_to=get_image_path)
    class Kind(Enum):
        EXPERIMENT = 1
        BUY = 2
        SELL = 3

    def kind(self):
        if self.kind_buffer is not None:
            return self.kind_buffer

        try:
            self.buydata
            self.kind_buffer = self.Kind.BUY
            return self.kind_buffer
        except self.DoesNotExist:
            pass

        try:
            self.selldata
            self.kind_buffer = self.Kind.SELL
            return self.kind_buffer
        except self.DoesNotExist:
            pass

        try:
            self.experiencedata
            self.kind_buffer = self.Kind.EXPERIMENT
            return self.kind_buffer
        except self.DoesNotExist:
            pass

    def stock_data(self):
        return self.stock

    def owner_data(self):
        return self.owner

    def clean(self, *args, **kwargs):
        super().clean(*args, **kwargs)

    def save(self, *args, **kwargs):
        """
        It overrides the django models save.

        On save, we update the timestamp of the creation date. It is only updated if there isn't a value defined.
          So it will not be changed on updates.

        """
        # For now we force an account for speed development. Later we can remove
        # this and let for the interface manage the account
        try:
            self.account
        except Account.DoesNotExist:
            self.account = Account.objects.all().order_by('-pk')[0]

        if self.analysis is None:
            analysis = Analysis()
            analysis.save()
            self.analysis = analysis

        if not self.creation_date:
            self.creation_date = datetime.now()

        if self.executed and not self.execution_date:
            self.execution_date = datetime.now()

        pre_category = None
        if self.category == 'NA':

            if self.executed is True:
                utc = pytz.UTC
                today_utc = utc.localize(datetime.today())
                day_today = utc.localize(datetime(today_utc.year, today_utc.month, today_utc.day))

                try:
                    past_operation = utc.localize(self.execution_date) < day_today
                except(ValueError):
                    past_operation = self.execution_date < day_today


                pre_category = self.operation_category()
                if past_operation:
                    self.category = pre_category

        super().save(*args, **kwargs)

    def operation_average_price(self, price=None):
        """
        This is the price of the stock with all the costs and taxes attributed.

        More information can be found in the `Bussola
        <http://blog.bussoladoinvestidor.com.br/calculo-do-preco-medio-de-acoes/>`_.


        :param reference_date: The date to cut until when the operations will be considered.

        :returns: The average price
        :rtype: Decimal
        """
        if not price:
            price = self.price

        return Decimal(support_system_formulas.calculate_average_price(self.amount,
                                                                       price,
                                                                       self.operation_cost()))

    def average_cost(self):
        """
        The cost but using the average price

        :returns: The average cost of the operation
        :rtype: Decimal
        """
        return Decimal(support_system_formulas.calculate_price(self.amount, self.operation_average_price()))

    def cost(self):
        """
        The cost of this operation stock.

        The price of the operation is a raw value, it only multiplies the amount for the value.And don't care about
                taxes or operation costs.


        :returns: The price of the operation
        :rtype: Decimal
        """
        return Decimal(support_system_formulas.calculate_price(self.amount,
                                                               self.price))

    def average_stock_cost(self):
        return Decimal(support_system_formulas.calculate_price(self.amount, self.operation_average_price(self.stock.price)))

    def stock_cost(self):
        return Decimal(support_system_formulas.calculate_price(self.amount, self.stock.price))

    def calculate_gain(self, sell_price=None, buy_price=None):
        """
        Internal method that calculates the gain based on any sell price

        In the calculations must be considered the cost of the operations, as well as all the other tributes.

        Arguments:

        :param stock_sell_price: A value that will be converted to decimal and be used in the calculation.


        :returns: The gain
        :rtype: Decimal

        """
        try:
            if sell_price is None:
                return None

            if buy_price is None:
                buy_price=self.price

            return Decimal(support_system_formulas.calculate_gain(Decimal(sell_price),
                                                                  buy_price, self.amount,
                                                                  self.operation_cost())).quantize( Decimal('.05'),
                                                                                                   rounding=ROUND_DOWN)
        except TypeError:
            return None

    def gain_per_stock(self):
        if self.kind() is self.Kind.EXPERIMENT:
            return self.experiencedata.gain_per_stock()

        if self.kind() is self.Kind.SELL:
            return self.selldata.gain_per_stock()

        return self.price - self.stock.price

    def calculate_gain_percent(self, sell_price=None, buy_price=None):
        if sell_price is None:
            return None

        if buy_price is None:
            buy_price = self.price

        return Decimal(support_system_formulas.calculate_gain_percent(
            Decimal(sell_price),
            Decimal(buy_price),
            Decimal(self.amount),
            Decimal(self.operation_cost())))

    def suggest_category(self, kind=None):
        if self.is_daytrade(kind):
            return 'DT'

        if self.amount % 100 != 0:
            return 'F'

        return 'O'

    def operation_category(self, kind=None):
        if self.category != 'NA':
            return self.category

        if self.is_daytrade(kind):
            return 'DT'

        if self.amount % 100 != 0:
            return 'F'

        return 'O'

    def operation_category_display(self, kind=None):
        operation_category = self.operation_category(kind)
        return dict(self.CATEGORY).get(operation_category)

    def categories(self):
        return self.CATEGORY

    def category_display(self):
        """
        Returns the actual saved category display text.
        """
        return self.get_category_display()

    def operation_cost(self, kind=None):
        if self.operation_category(kind) == 'F':
            return self.account.operation_cost_fraction

        if self.operation_category(kind) == 'DT':
            return self.account.operation_cost_day_trade

        return self.account.operation_cost_position

    def is_daytrade(self, kind=None):
        """
        When there is an operation of sell occurring in the same
        day of an operation of buy in the same account, this is a daytrade
        operation.

        TODO: We are based on the sell because for now we dont work with rent
        trade.
        """
        if self.dt_result is not None:
            return self.dt_result

        if kind is None:
            kind = self.kind()

        if kind is self.Kind.SELL:
            reference_date = datetime.now()
            if self.execution_date:
                reference_date = self.execution_date

            day_buys = Operation.objects.filter(buydata__isnull=False).filter(stock=self.stock).filter(account=self.account).filter(execution_date__day=reference_date.day, execution_date__month=reference_date.month, execution_date__year=reference_date.year, execution_date__lte=reference_date)

            self.dt_result = day_buys.count() > 0

            return self.dt_result

        if kind is self.Kind.BUY:
            if self.execution_date:
                day_sells = Operation.objects.filter(selldata__isnull=False).filter(stock=self.stock).filter(account=self.account).filter(execution_date__day=self.execution_date.day, execution_date__month=self.execution_date.month, execution_date__year=self.execution_date.year, execution_date__lte=self.execution_date)

                self.dt_result = day_sells.count() > 0
            else:
                self.dt_result = False
            return self.dt_result

        self.dt_result = False
        return False
