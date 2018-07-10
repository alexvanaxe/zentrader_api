"""
Allow the complex data from the model instance of the account to be converted to native Python datatypes,
that can then be easily rendered into JSON, XML or other content types.
Also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the
incoming data.
"""
from rest_framework import serializers

class IrBrSerializer(serializers.Serializer):
    ir = serializers.DecimalField(max_digits=22, decimal_places=2)
    ir_daytrade = serializers.DecimalField(max_digits=22, decimal_places=2)
