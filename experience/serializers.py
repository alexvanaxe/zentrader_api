"""
Allow the complex data from the model instance of the account to be converted to native Python datatypes,
that can then be easily rendered into JSON, XML or other content types.
Also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the
incoming data.
"""
from rest_framework import serializers

from experience.models import ExperienceData
from stock.serializers import StockSerializer
from zen_oauth.serializers import UserSerializer
from operation.exceptions import NegativeStocksError


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


class ExperienceDataSerializer(serializers.ModelSerializer):
    """
    Serializer for ExperienceData model.
    """

    stock_data = StockSerializer(read_only=True)
    detailed = serializers.BooleanField('detailed', default=False)
    category = serializers.CharField(label='category', max_length=2, default='NA')

    class Meta:
        fields = ('pk', 'owner', 'category', 'creation_date', 'stock', 'amount',
                  'price', 'archived', 'nickname', 'favorite', 'limit',
                  'stop_gain', 'stop_loss', 'estimated_date', 'target',
                  'favorite', 'get_intent_display', 'intent', 'stock_data',
                  'action', 'detailed')
        read_only_fields = ('creation_date', 'detailed', 'owner')
        model = ExperienceData

        validators = [NegativeStocksValidator(), ]


class ExperienceDataSerializerDetailed(serializers.ModelSerializer):
    """
    Serializer for ExperienceData model.
    """

    stock_data = StockSerializer(read_only=True)
    detailed = serializers.BooleanField('detailed', default=True)
    owner_data = UserSerializer(read_only=True)
    category = serializers.CharField(label='category', max_length=2, default='NA')

    class Meta:
        fields = ('pk', 'owner', 'owner_data', 'creation_date', 'stock', 'amount', 'price', 'archived',
                  'nickname', 'category', 'category_display', 'categories', 'limit', 'stop_gain', 'stop_loss',
                  'target', 'get_intent_display', 'intent', 'intents', 'stock_data', 'action', 'target_gain',
                  'detailed', 'operation_limit', 'cost', 'stock_cost', 'operation_average_price',
                  'average_cost', 'average_stock_cost', 'target_gain_total_percent',
                  'target_gain_percent', 'experience_gain', 'experience_gain_percent',
                  'experience_total_gain_percent', 'favorite', 'stop_loss_result',
                  'stop_loss_percent', 'stop_loss_total_percent', 'estimated_date')
        read_only_fields = ('creation_date', 'owner', 'owner_data', 'operation_gain', 'detailed', 'target_gain', 'operation_limit',
                            'cost', 'stock_cost', 'operation_average_price', 'average_cost',
                            'average_stock_cost', 'target_gain_total_percent', 'target_gain_percent',
                            'experience_gain', 'experience_gain_percent', 'experience_total_gain_percent',
                            'stop_loss_result', 'stop_loss_percent', 'intents',
                            'stop_loss_total_percent', 'categories', 'category_display')
        model = ExperienceData

        validators = [NegativeStocksValidator(), ]
