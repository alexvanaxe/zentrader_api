from datetime import datetime
from django.db import models

from django.utils.translation import gettext_lazy as _


class Note(models.Model):
    operation = models.ForeignKey('operation.Operation', on_delete=models.CASCADE)

    note = models.TextField(_('note'), null=True, blank=True, max_length=140)
    creation_date = models.DateTimeField(_('creation date'), null=False, editable=False)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.now()

        super().save(*args, **kwargs)
