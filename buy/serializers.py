"""
Allow the complex data from the model instance of the account to be converted to native Python datatypes,
that can then be easily rendered into JSON, XML or other content types.
Also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the
incoming data.
"""

from rest_framework import serializers

from buy.models import BuyData
from account.models import Account
from stock.serializers import StockSerializer
from zen_oauth.serializers import UserSerializer
from operation.exceptions import NotEnoughMoney, NegativeStocksError


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


class MoneyValidator(object):
    def __init__(self, queryset, fields):
        self.account = queryset
        self.instance = None

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
    owner_data = UserSerializer(read_only=True)
    # sell_set = SellDataSerializer(read_only=True, many=True)

    class Meta:
        fields = ('pk', 'owner', 'owner_data', 'experience', 'creation_date', 'stock', 'amount', 'price',
                  'archived', 'executed', 'nickname', 'category', 'category_display', 'categories',
                  'favorite', 'stock_data', 'operation_gain',
                  'operation_average_price', 'average_cost', 'average_stock_cost', 'cost',
                  'operation_gain_percent', 'amount_available')
        read_only_fields = ('creation_date', 'owner', 'owner_data', 'stock_data', 'operation_gain',
                            'operation_average_price', 'average_cost',
                            'average_stock_cost', 'cost', 'operation_gain_percent', 'amount_available', 'categories', 'category_display')
        model = BuyData

        validators = [MoneyValidator(queryset=Account.objects.all(),
                                    fields=['pk', 'price', 'amount', ]), NegativeStocksValidator()]
