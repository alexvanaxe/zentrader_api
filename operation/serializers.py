"""
Allow the complex data from the model instance of the account to be converted to native Python datatypes,
that can then be easily rendered into JSON, XML or other content types.
Also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the
incoming data.
"""
from rest_framework import serializers

from operation.models import ExperienceData, BuyData, SellData
from stock.serializers import StockSerializer


class ExperienceDataSerializer(serializers.ModelSerializer):
    """
    Serializer for ExperienceData model.
    """

    stock_data = StockSerializer(read_only=True)
    class Meta:
        fields = ('pk', 'stock', 'date', 'amount', 'price', 'archived',
                  'nickname', 'favorite', 'limit', 'stop_gain', 'stop_loss',
                  'target', 'stock_data', 'action', 'target_gain', 'operation_limit')
        read_only_fields = ('operation_gain', 'operation_limit')
        model = ExperienceData


class BuyDataSerializer(serializers.ModelSerializer):
    """
    Serializer for BuyDataSerializer model.
    """
    stock_data = StockSerializer(read_only=True)

    class Meta:
        fields = ('pk', 'stock', 'date', 'amount', 'price', 'archived',
                  'nickname', 'favorite', 'stock_data', 'operation_gain')
        model = BuyData


class SellDataSerializer(serializers.ModelSerializer):
    """
    Serializer for SellDataSerializer model.
    """
    class Meta:
        fields = ('pk', 'stock', 'date', 'amount', 'price', 'archived',
                  'nickname', 'favorite', 'value')
        model = SellData


#  class OperationCostSerializer(serializers.Serializer):
#      def create(self, validated_data):
#          pass
#
#      def update(self, instance, validated_data):
#          pass
#
#      cost = serializers.DecimalField(read_only=True, max_digits=22, decimal_places=2)
