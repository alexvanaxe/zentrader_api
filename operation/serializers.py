"""
Allow the complex data from the model instance of the account to be converted to native Python datatypes,
that can then be easily rendered into JSON, XML or other content types.
Also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the
incoming data.
"""
from rest_framework import serializers


class ArchiveSerializer(serializers.Serializer):
    pk = serializers.IntegerField(label='ID', read_only=True)
    archived = serializers.BooleanField(label='archived')

    def save(self, instance):
        instance.archived = True
        instance.save()

        return instance
