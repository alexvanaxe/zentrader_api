"""
Allow the complex data from the model instance of the account to be converted to native Python datatypes,
that can then be easily rendered into JSON, XML or other content types.
Also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the
incoming data.
"""
from rest_framework import serializers

from operation.models import ExperienceData, BuyData, SellData
from account.models import Account
from stock.serializers import StockSerializer
from operation.exceptions import NotEnoughMoney, NotEnoughStocks, OperationExecuted, NegativeStocksError


class MoneyValidator(object):
    def __init__(self, queryset, fields):
        self.account = queryset

    def __call__(self, value):
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
    def __init__(self):
        pass

    def __call__(self, value):
        amount_requested = 0
        try:
            amount_requested = value['amount']
        except KeyError:
            return

        if amount_requested <= 0:
            raise NegativeStocksError()

    def set_context(self, serializer):
        self.instance = getattr(serializer, 'instance', None)


class SellValidator(object):
    def __init__(self):
        pass

    def __call__(self, value):
        amount_edited = 0
        try:
            amount = value['amount']
            amount_edited = amount
        except KeyError:
            amount = self.instance.amount

        try:
            amount_available = value['buy'].amount_available(executed_filter=None)
        except KeyError:
            amount_available = self.instance.amount_available(executed_filter=None)


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


class ExecutedValidator(object):
    def __init__(self):
        pass

    def __call__(self, value):
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
    class Meta:
        fields = ('pk', 'buy', 'executed', 'stock', 'creation_date', 'amount', 'price', 'archived',
                  'nickname', 'favorite', 'stop_gain', 'stop_loss', 'amount_available', 'stock_data',
                  'sell_value', 'profit', 'profit_percent', 'profit_total_percent',
                  'stock_profit', 'stock_profit_total_percent', 'stock_profit_percent',
                  'stock_data', 'stop_loss_result', 'stop_loss_percent', 'stop_loss_total_percent',
                  'stop_gain_result', 'stop_gain_percent', 'amount_available')
                    # result
        read_only_fields = ('stock_data', 'sell_value', 'result', 'gain_percent',
                            'profit', 'profit_percent', 'profit_total_percent', 'amount_available', 'stock_data',
                            'sell_value', 'profit', 'profit_percent', 'profit_total_percent',
                            'stock_profit', 'stock_profit_total_percent', 'stock_profit_percent',
                            'stock_data', 'stop_loss_result', 'stop_loss_percent', 'stop_loss_total_percent',
                            'stop_gain_result', 'stop_gain_percent', 'amount_available')
        model = SellData

        validators = [ExecutedValidator(), SellValidator(), NegativeStocksValidator()]


class BuyDataSerializer(serializers.ModelSerializer):
    """
    Serializer for BuyDataSerializer model.
    """
    stock_data = StockSerializer(read_only=True)
    # sell_set = SellDataSerializer(read_only=True, many=True)

    class Meta:
        fields = ('pk', 'experience', 'creation_date', 'stock', 'amount', 'price',
                  'archived', 'executed', 'nickname', 'favorite', 'stock_data', 'operation_gain',
                  'operation_average_price', 'average_cost', 'average_stock_cost', 'cost',
                  'operation_gain_percent', 'amount_available')
        read_only_fields = ('creation_date', 'stock_data', 'operation_gain',
                            'operation_average_price', 'average_cost',
                            'average_stock_cost', 'cost', 'operation_gain_percent', 'amount_available')
        model = BuyData

        validators = [MoneyValidator(queryset=Account.objects.all(),
                                    fields=['pk', 'price', 'amount', ]), NegativeStocksValidator()]


class ExperienceDataSerializer(serializers.ModelSerializer):
    """
    Serializer for ExperienceData model.
    """

    stock_data = StockSerializer(read_only=True)
    detailed = serializers.BooleanField('detailed', default=False)

    class Meta:
        fields = ('pk', 'creation_date', 'stock', 'amount', 'price', 'archived',
                  'nickname', 'favorite', 'limit', 'stop_gain', 'stop_loss',
                  'target', 'favorite', 'get_intent_display', 'stock_data', 'action',
                  'detailed')
        read_only_fields = ('creation_date', 'detailed')
        model = ExperienceData

        validators = [NegativeStocksValidator(), ]


class ExperienceDataSerializerDetailed(serializers.ModelSerializer):
    """
    Serializer for ExperienceData model.
    """

    stock_data = StockSerializer(read_only=True)
    detailed = serializers.BooleanField('detailed', default=True)

    class Meta:
        fields = ('pk', 'creation_date', 'stock', 'amount', 'price', 'archived',
                  'nickname', 'favorite', 'limit', 'stop_gain', 'stop_loss',
                  'target', 'favorite', 'get_intent_display', 'stock_data', 'action', 'target_gain',
                  'detailed', 'operation_limit', 'cost', 'stock_cost', 'operation_average_price',
                  'average_cost', 'average_stock_cost', 'target_gain_total_percent',
                  'target_gain_percent', 'experience_gain', 'experience_gain_percent',
                  'experience_total_gain_percent', 'favorite', 'stop_loss_result',
                  'stop_loss_percent', 'stop_loss_total_percent')
        read_only_fields = ('creation_date', 'operation_gain', 'detailed', 'target_gain', 'operation_limit',
                            'cost', 'stock_cost', 'operation_average_price', 'average_cost',
                            'average_stock_cost', 'target_gain_total_percent', 'target_gain_percent',
                            'experience_gain', 'experience_gain_percent', 'experience_total_gain_percent',
                            'favorite', 'stop_loss_result', 'stop_loss_percent',
                            'stop_loss_total_percent')
        model = ExperienceData

        validators = [NegativeStocksValidator(), ]


class RiskDataSerializer(serializers.Serializer):
    shark = serializers.DecimalField(max_digits=22, decimal_places=2)


class ArchiveSerializer(serializers.Serializer):
    pk = serializers.IntegerField(label='ID', read_only=True)
    archived = serializers.BooleanField(label='archived')

    def save(self, instance):
        instance.archived = True
        instance.save()

        return instance
