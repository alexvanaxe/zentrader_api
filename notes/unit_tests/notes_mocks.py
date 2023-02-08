from datetime import datetime

from experience.models import ExperienceData
from account.models import Account
from notes.models import Note

def create_notes(cls, operation):
    """
    Creates some notes
    """
    cls.note1 = Note.objects.create(operation=operation, note="Note 1")
    cls.note2 = Note.objects.create(operation=operation, note="Note 2")
