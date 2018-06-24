from datetime import datetime

from decimal import Decimal, ROUND_DOWN
from django.db import models

from django.utils.translation import ugettext_lazy as _

# def get_image_path(instance, filename):
#     """ Get the path where the images are stored in the filesystem """
#     return os.path.join('charts', str(instance.transaction.id), instance.operation_status.name,
#                         str(time.mktime(instance.creation_date.timetuple())), filename)
from account.models import Account
from formulas import support_system_formulas


class Operation(models.Model):
    """ A operation realized in a transaction (ex: buy, sell, experiment...) """

    class Meta:
        abstract = True

    IS_ARCHIVED = (
        ('Y', _('Yes')),
        ('N', _('No'))
    )

    FAVORITE = (
        ('Y', _('Yes')),
        ('N', _('No'))
    )

    def __str__(self):
        return str(self.pk)

    account = models.ForeignKey('account.Account', on_delete=models.CASCADE)
    stock = models.ForeignKey('stock.Stock', on_delete=models.CASCADE)
    date = models.DateTimeField(_('oparation date'), null=False)
    creation_date = models.DateTimeField(_('creation date'), null=False, editable=False)
#    chart = models.ImageField(_('chart graph'), null=True, blank=True, upload_to=get_image_path)
    amount = models.DecimalField(_('amount'), max_digits=22, decimal_places=0, null=False, blank=False)
    # The value of the stock at the moment of the operation
    price = models.DecimalField(_('stock value'), max_digits=22, decimal_places=2, null=False, blank=False)
#    tunnel_bottom = models.DecimalField(_('Bottom tunnel'), max_digits=22, decimal_places=2, null=True, blank=True)
#    tunnel_top = models.DecimalField(_('Top tunnel'), max_digits=22, decimal_places=2, null=True, blank=True)
    archived = models.BooleanField(_('archived'), default=False)
    nickname = models.TextField(_('nickname'), null=True, blank=True,
                                max_length=100)

    favorite = models.CharField(_('favorite'), max_length=1, choices=FAVORITE, default='N')

    def stock_data(self):
        return self.stock

    def save(self, *args, **kwargs):
        """
        It overrides the django models save.

        On save, we update the timestamp of the creation date. It is only updated if there isn't a value defined.
          So it will not be changed on updates.

        """
        if not self.creation_date:
            self.creation_date = datetime.now()

        # For now we force an account for speed development. Later we can remove
        # this and let for the interface manage the account
        try:
            self.account
        except Account.DoesNotExist:
            self.account = Account.objects.all()[0]

        super().save(*args, **kwargs)

    def operation_average_price(self):
        """
        This is the price of the stock with all the costs and taxes attributed.

        More information can be found in the `Bussola
        <http://blog.bussoladoinvestidor.com.br/calculo-do-preco-medio-de-acoes/>`_.


        :param reference_date: The date to cut until when the operations will be considered.

        :returns: The average price
        :rtype: Decimal
        """
        return Decimal(support_system_formulas.calculate_average_price(self.amount,
                                                               self.price,
                                                               self.account.operation_cost))

    def average_cost(self):
        """
        The cost but using the average price

        :returns: The average cost of the operation
        :rtype: Decimal
        """
        return Decimal(support_system_formulas.calculate_price(self.amount,
                       support_system_formulas.calculate_average_price(self.amount,
                                                               self.price,
                                                               self.account.operation_cost)))

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
        return Decimal(support_system_formulas.calculate_price(self.amount,
                       support_system_formulas.calculate_average_price(self.amount,
                                                               self.stock.price,
                                                               self.account.operation_cost)))

    def stock_cost(self):
        return Decimal(support_system_formulas.calculate_price(self.amount,
                                                               self.stock.price))


    def calculate_gain(self, stock_sell_price=None):
        """
        Internal method that calculates the gain based of any sell price

        In the calculations must be considered the cost of the operations, as well as the other tributes.

        Arguments:

        :param stock_sell_price: A value that will be converted to decimal and be used in the calculation.


        :returns: The gain
        :rtype: Decimal

        """
        operation_paid = (Account.objects.all()[0]).operation_cost

        try:
            return Decimal(support_system_formulas.calculate_gain(Decimal(stock_sell_price), self.price, self.amount,
                                                                  operation_paid)).quantize(
                Decimal('.05'), rounding=ROUND_DOWN)
        except TypeError:
            return None


class ExperienceData(Operation):
    """ Some additional data and functions specifics for the experiments """

    def __str__(self):
        return str(self.amount)
    target = models.DecimalField(_('target price'), max_digits=22, decimal_places=2, null=True, blank=True)
    stop_gain = models.DecimalField(_('stop gain'), max_digits=22, decimal_places=2, null=True, blank=True)
    stop_loss = models.DecimalField(_('stop loss'), max_digits=22, decimal_places=2, null=True, blank=True)
    limit = models.DecimalField(_('limit'), max_digits=6, decimal_places=2, null=True, blank=True)
    action = models.TextField(_('action'), null=True, blank=True, max_length=140)

    def target_gain(self):
        """
        Calculate the gain based in the stock value.

        Make use of the internal _calculate_gain of the operation.


        :returns: The gain
        :rtype: Decimal

        """
        return self.calculate_gain(self.target)

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

        account = (Account.objects.all()[0])
        return Decimal(support_system_formulas.calculate_limit(support_system_formulas.PIRANHA_LIMIT,
                                                               account.equity,
                                                               account.operation_cost,
                                                               self.stop_loss,
                                                               self.amount))


class BuyData(Operation):
    def operation_gain(self):
        """
        Calculate the gain based in the stock value.

        Make use of the internal _calculate_gain of the operation.


        :returns: The gain
        :rtype: Decimal

        """
        return self.calculate_gain(self.stock.price)


class SellData(Operation):
    pass
