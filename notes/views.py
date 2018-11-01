from django.shortcuts import render

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from notes.models import Note
from notes.serializers import NoteSerializer

# Create your views here.
class NotesModelViewSet(viewsets.ModelViewSet):
    """
    A Model View Set representing the Notes.
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('operation', )
