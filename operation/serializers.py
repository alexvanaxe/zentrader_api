"""
Allow the complex data from the model instance of the account to be converted to native Python datatypes,
that can then be easily rendered into JSON, XML or other content types.
Also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the
incoming data.
"""
from rest_framework import serializers

from operation.models import ExperienceData, BuyData, SellData
from account.models import Account
from stock.models import Stock
from stock.serializers import StockSerializer
from operation.exceptions import NotEnoughMoney, NotEnoughStocks


class ExperienceDataSerializer(serializers.ModelSerializer):
    """
    Serializer for ExperienceData model.
    """

    stock_data = StockSerializer(read_only=True)
    class Meta:
        fields = ('pk', 'creation_date', 'stock', 'amount', 'price', 'archived',
                  'nickname', 'favorite', 'limit', 'stop_gain', 'stop_loss',
                  'target', 'stock_data', 'action', 'target_gain',
                  'operation_limit', 'intent', 'cost', 'stock_cost',
                  'operation_average_price', 'average_cost',
                  'average_stock_cost', 'target_gain_percent',
                  'experience_gain', 'experience_gain_percent', 'favorite',
                  'get_intent_display', 'stop_loss_result','stop_loss_percent')
        read_only_fields = ('creation_date', 'operation_gain', 'operation_limit', 'cost',
                            'real_cost', 'operation_average_price',
                            'average_cost', 'average_stock_cost',
                            'target_gain_percent', 'experience_gain',
                            'experience_gain_percent', 'get_intent_display',
                            'stop_loss_result','stop_loss_percent')
        model = ExperienceData


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


class BuyDataSerializer(serializers.ModelSerializer):
    """
    Serializer for BuyDataSerializer model.
    """
    stock_data = StockSerializer(read_only=True)

    class Meta:
        fields = ('pk', 'creation_date', 'stock', 'amount', 'price', 'archived',
                  'nickname', 'favorite', 'stop_gain', 'stop_loss', 'stock_data', 'operation_gain',
                  'operation_average_price', 'average_cost',
                  'average_stock_cost', 'cost', 'operation_gain_percent',
                  'stop_loss_result','stop_loss_percent',
                  'stop_gain_result','stop_gain_percent')
        read_only_fields = ('creation_date', 'stock_data', 'operation_gain',
                            'operation_average_price', 'average_cost',
                            'average_stock_cost', 'cost',
                            'operation_gain_percent', 'stop_loss_result',
                            'stop_loss_percent', 'stop_gain_result','stop_gain_percent')
        model = BuyData

        validators = MoneyValidator(queryset=Account.objects.all(),
                                    fields=['pk', 'price', 'amount', ]),

class SellValidator(object):
    def __init__(self):
        pass

    def __call__(self, value):
        amount = value['amount']
        stocks = value['stock'].owned()

        if stocks < amount:
            raise NotEnoughStocks()

class SellDataSerializer(serializers.ModelSerializer):
    """
    Serializer for SellDataSerializer model.
    """
    class Meta:
        fields = ('pk', 'stock', 'amount', 'price', 'archived',
                  'nickname', 'favorite')
        model = SellData

        validators = SellValidator(),

class RiskDataSerializer(serializers.Serializer):
    shark = serializers.DecimalField(max_digits=22, decimal_places=2)


