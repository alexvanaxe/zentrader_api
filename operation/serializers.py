"""
Allow the complex data from the model instance of the account to be converted to native Python datatypes,
that can then be easily rendered into JSON, XML or other content types.
Also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the
incoming data.
"""
from rest_framework import serializers

from operation.models import Operation, ExperienceData, OperationType, BuyData, SellData
from stock.serializers import StockSerializer


class OperationSerializer(serializers.ModelSerializer):
    """
    Serializer for Operation model.
    """

    class Meta:
        model = Operation
        fields = ('pk', 'amount', 'creation_date', 'date', 'favorite',
                  'operation_type', 'price', 'stock', 'cost', 'archived')
        read_only_fields = ('creation_date', 'cost')


class OperationTypeSerializer(serializers.ModelSerializer):
    """
    A serializer to serialize the operation type data. It is a read only serializer.
    """
    class Meta:
        model = OperationType
        read_only_fields = ('pk', 'name',)
        fields = ('pk', 'name',)


class OperationNestedSerializer(OperationSerializer):
    """
    Serializer for Operation model.
    """
    stock = StockSerializer(read_only=True)
    operation_type = OperationTypeSerializer(read_only=True)


class ExperienceDataSerializer(serializers.ModelSerializer):
    """
    Serializer for ExperienceData model.
    """
    class Meta:
        fields = ('pk', 'operation', 'limit', 'stop_gain', 'stop_loss', 'target', 'operation_gain', 'operation_limit')
        read_only_fields = ('operation_gain', 'operation_limit')
        model = ExperienceData


class ExperienceDataNSerializer(ExperienceDataSerializer):
    """
    Nested Experience Serializer. It is intended to be read only
    """
    operation = OperationNestedSerializer(read_only=True)


class BuyDataSerializer(serializers.ModelSerializer):
    """
    Serializer for BuyDataSerializer model.
    """
    class Meta:
        fields = ('pk', 'operation')
        model = BuyData


class BuyDataNSerializer(BuyDataSerializer):
    """
    Nested Buy Serializer. It is intended to be read only
    """
    operation = OperationNestedSerializer(read_only=True)


class SellDataSerializer(serializers.ModelSerializer):
    """
    Serializer for SellDataSerializer model.
    """
    class Meta:
        fields = ('pk', 'operation', 'value')
        model = SellData


class SellDataNSerializer(SellDataSerializer):
    """
    Nested Sell Serializer. It is intended to be read only
    """
    operation = OperationNestedSerializer(read_only=True)


class OperationCostSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    cost = serializers.DecimalField(read_only=True, max_digits=22, decimal_places=2)



