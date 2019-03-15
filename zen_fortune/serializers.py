"""
Allow the complex data from the model instance of the account to be converted to native Python datatypes,
that can then be easily rendered into JSON, XML or other content types.
Also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the
incoming data.
"""
from rest_framework import serializers


class ZenFortuneSerializer(serializers.Serializer):
    """
    Serialize a fortune cookie to bring us fortune
    """
    cookie = serializers.CharField(label='Name', max_length=10000)
