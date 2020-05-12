"""
Allow the complex data from the model instance of the account to be converted to native Python datatypes,
that can then be easily rendered into JSON, XML or other content types.
Also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the
incoming data.
"""
from rest_framework import serializers


class ReportTotalProfitSerializer(serializers.Serializer):
    """
    Serializer from the total profit accumulated from all times
    """
    total_profit = serializers.DecimalField(max_digits=22, decimal_places=2)
