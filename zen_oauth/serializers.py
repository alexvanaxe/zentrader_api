"""
Allow the complex data from the model instance of the account to be converted to native Python datatypes,
that can then be easily rendered into JSON, XML or other content types.
Also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the
incoming data.
"""
from rest_framework import serializers

from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """ The serializer for the user info """

    class Meta:
        model = User
        fields = ('id', 'username')
