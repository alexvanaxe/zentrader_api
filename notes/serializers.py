"""
Allow the complex data from the model instance of the account to be converted to native Python datatypes,
that can then be easily rendered into JSON, XML or other content types.
Also provide deserialization, allowing parsed data to be converted back into complex types, after first validating the
incoming data.
"""

from rest_framework import serializers
from notes.models import Note

class NoteSerializer(serializers.ModelSerializer):
    """
    Serializer for the notes.
    """
    class Meta(object):
        """
        The meta informations for the Notes Serializer.
        It contains all the fields. And all the fields are writable.
        """

        fields = ('pk', 'operation', 'note', 'creation_date')
        read_only_fields = ('creation_date', )
        model = Note
