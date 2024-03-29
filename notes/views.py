from django.shortcuts import render

from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from notes.models import Note
from notes.serializers import NoteSerializer


class NotesModelViewSet(viewsets.ModelViewSet):
    """
    A Model View Set representing the Notes.
    """
    queryset = Note.objects.all().order_by('-pk')
    serializer_class = NoteSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['operation']
