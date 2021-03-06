"""
Allow the complex data from the model instance of the account to be converted to native Python datatypes,
that can then be easily rendered into JSON, XML or other content types.
Also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the
incoming data.
"""
from rest_framework import serializers
import stock.serializers as stockserializers

import learning.models as models


class PaperBuySerializer(serializers.ModelSerializer):
    """
    Serializer for PaperBuySerializer model.
    """

    stock_data = stockserializers.StockSerializer(read_only=True)

    class Meta:
        """ The meta instructions of the serializer. """
        fields = ('pk', 'experience', 'creation_date', 'stock', 'amount',
                  'price', 'archived', 'nickname', 'stock_data', 'papersell_set')
        read_only_fields = ('creation_date', 'stock_data', 'papersell_set')
        model = models.PaperBuy


class PaperSellSerializer(serializers.ModelSerializer):
    """
    Serializer for PaperSellSerializer model.
    """

    stock_data = stockserializers.StockSerializer(read_only=True)

    class Meta:
        fields = ('pk', 'paper_buy', 'creation_date', 'stock', 'amount', 'price',
                  'archived', 'nickname', 'stop_loss', 'stop_gain', 'stock_data',
                  'sell_gain', 'sell_gain_percent')
        read_only_fields = ('creation_date', 'stock_data', 'sell_gain', 'sell_gain_percent')
        model = models.PaperSell
