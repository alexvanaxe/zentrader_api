from django.shortcuts import render

from rest_framework import viewsets

from notes.models import Note
from notes.serializers import NoteSerializer

# Create your views here.
class NotesModelViewSet(viewsets.ModelViewSet):
    """
    A Model View Set representing the Notes.
    """
    queryset = Note.objects.all()
    serializer_class = NoteSerializer
