"""
Allow the complex data from the model instance of the account to be converted to native Python datatypes,
that can then be easily rendered into JSON, XML or other content types.
Also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the
incoming data.
"""
from rest_framework import serializers
from account.models import Account


class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for Account model.
    """
    class Meta:
        model = Account
        fields = ('pk', 'broker', 'operation_cost_day_trade', 'operation_cost_fraction',
                  'operation_cost_position', 'equity')
        #  read_only_fields = ('', )
