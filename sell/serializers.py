"""
Allow the complex data from the model instance of the account to be converted
to native Python datatypes,
that can then be easily rendered into JSON, XML or other content types.
Also provide deserialization, allowing parsed data to be converted back into
complex types, after first validating the incoming data.
"""
from rest_framework import serializers

from sell.models import SellData
from stock.serializers import StockSerializer
from zen_oauth.serializers import UserSerializer
from operation.exceptions import NotEnoughMoney, NotEnoughStocks,\
    OperationExecuted, NegativeStocksError


class SellValidator(object):
    requires_context = True
    def __init__(self):
        pass

    def __call__(self, value, serializer_field):
        self.set_context(serializer_field)
        amount_edited = 0
        try:
            amount = value['amount']
            amount_edited = amount
        except KeyError:
            amount = self.instance.amount

        try:
            if value['buy'] is not None:
                amount_available = value['buy'].amount_available(
                    executed_filter=None)
            else:
                amount_available = self.instance.amount_available(
                    executed_filter=None)
        except KeyError:
            amount_available = self.instance.amount_available(
                executed_filter=None)

        if self.instance:
            amount_available = amount_available + self.instance.amount
            if amount_edited <= self.instance.amount:  # He wants to reduce the stocks
                return

        if (amount > amount_available):
            raise NotEnoughStocks()

    def set_context(self, serializer):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # Determine the existing instance, if this is an update operation.
        self.instance = getattr(serializer, 'instance', None)


class MoneyValidator(object):
    requires_context = True
    def __init__(self, queryset, fields):
        self.account = queryset
        self.instance = None

    def __call__(self, value, serializer_field):
        self.set_context(serializer_field)
        if self.instance is None or not self.instance.pk:
            cost = value['amount'] * value['price']
            account_selected = self.account.order_by('-pk')[0]
            if cost > account_selected.equity:
                raise NotEnoughMoney()

    def set_context(self, serializer):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # Determine the existing instance, if this is an update operation.
        self.instance = getattr(serializer, 'instance', None)


class NegativeStocksValidator(object):
    """ Validate if the value is greater than zero """
    requires_context = True
    def __init__(self):
        self.instance = None

    def __call__(self, value, serializer_field):
        self.set_context(serializer_field)
        amount_requested = 0
        try:
            amount_requested = value['amount']
        except KeyError:
            return

        if amount_requested <= 0:
            raise NegativeStocksError()

    def set_context(self, serializer):
        self.instance = getattr(serializer, 'instance', None)


class ExecutedValidator(object):
    requires_context = True
    def __init__(self):
        self.instance = None

    def __call__(self, value, serializer_field):
        self.set_context(serializer_field)
        if self.instance and self.instance.pk:
            if self.instance.executed:
                raise OperationExecuted()

    def set_context(self, serializer):
        """
        This hook is called by the serializer instance,
        prior to the validation call being made.
        """
        # Determine the existing instance, if this is an update operation.
        self.instance = getattr(serializer, 'instance', None)


class SellDataSerializer(serializers.ModelSerializer):
    """
    Serializer for SellDataSerializer model.
    """
    stock_data = StockSerializer(read_only=True)
    owner_data = UserSerializer(read_only=True)

    class Meta:
        fields = ('pk', 'owner', 'owner_data', 'buy', 'analysis', 'buy_price',
                  'executed', 'stock', 'creation_date', 'amount', 'price',
                  'archived', 'nickname', 'favorite', 'category',
                  'category_display', 'categories', 'stop_gain', 'stop_loss',
                  'amount_available', 'stock_data', 'sell_value', 'profit',
                  'profit_percent', 'profit_total_percent', 'stock_profit',
                  'stock_profit_total_percent', 'stock_profit_percent',
                  'stock_data', 'stop_loss_result', 'stop_loss_percent',
                  'stop_loss_total_percent', 'suggest_category',
                  'stop_gain_result', 'stop_gain_percent', 'amount_available',
                  'operation_category', 'operation_category_display')

        read_only_fields = ('stock_data', 'owner_data', 'owner', 'buy_price',
                            'sell_value', 'result', 'gain_percent', 'profit',
                            'profit_percent', 'profit_total_percent',
                            'amount_available', 'stock_data', 'sell_value',
                            'profit', 'profit_percent', 'profit_total_percent',
                            'stock_profit', 'stock_profit_total_percent',
                            'stock_profit_percent', 'stock_data',
                            'stop_loss_result', 'stop_loss_percent',
                            'stop_loss_total_percent', 'stop_gain_result',
                            'stop_gain_percent', 'amount_available',
                            'suggest_category', 'categories',
                            'category_display', 'operation_category',
                            'operation_category_display')
        model = SellData

        validators = [ExecutedValidator(), SellValidator(), NegativeStocksValidator()]


class RiskDataSerializer(serializers.Serializer):
    shark = serializers.DecimalField(max_digits=22, decimal_places=2)
