"""
Allow the complex data from the model instance of the account to be converted to native Python datatypes,
that can then be easily rendered into JSON, XML or other content types.
Also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the
incoming data.
"""
from rest_framework import serializers
from stock.models import Stock


class StockSerializer(serializers.ModelSerializer):
    """
    Serializer for Stock model.
    """
    class Meta:
        model = Stock
        fields = ('pk', 'code', 'name', 'sector', 'subsector', 'price', 'owned')
        read_only_fields = ('owned', )

class OwnedStocksSerializer(serializers.Serializer):
    """
    The aggregation of the owned stocks. It contains the average price, which
    is used to know the total patrimonium.
    """
    code = serializers.CharField(max_length=5)
    name = serializers.CharField(label='Name', max_length=140)
    sector = serializers.CharField(label='Sector', max_length=140)
    subsector = serializers.CharField(label='Subsector', max_length=140)
    price = serializers.DecimalField(decimal_places=2, label='Stock value', max_digits=22)
    owned = serializers.ReadOnlyField(read_only=True)
    average_price = serializers.DecimalField(decimal_places=2, label='Average Price', max_digits=22)
    stock_value = serializers.DecimalField(decimal_places=2, label='Stock Value', max_digits=22)
    stock_result = serializers.DecimalField(decimal_places=2, label='Stock Result', max_digits=22)
    stock_result_percent = serializers.DecimalField(decimal_places=2, label='Stock Result Percent', max_digits=22)
    stock_result_total_percent = serializers.DecimalField(decimal_places=2, label='Stock Result Total Percent', max_digits=22)
    owner = serializers.CharField(label='username', max_length=140)
