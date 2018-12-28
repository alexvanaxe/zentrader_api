"""
Allow the complex data from the model instance of the account to be converted to native Python datatypes,
that can then be easily rendered into JSON, XML or other content types.
Also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the
incoming data.
"""
from rest_framework import serializers
import stock.serializers as StockSerializer

import learning.models as models



class PaperBuySerializer(serializers.ModelSerializer):
    """
    Serializer for PaperBuySerializer model.
    """

    class Meta:
        fields = ('pk', 'experience', 'creation_date', 'stock', 'amount', 'price',
                  'archived', 'nickname')
        read_only_fields = ('creation_date', )
        model = models.PaperBuy

