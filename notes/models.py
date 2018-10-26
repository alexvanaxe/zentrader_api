from django.db import models

from django.utils.translation import ugettext_lazy as _

# Create your models here.
class Note(models.Model):
    operation = models.ForeignKey('operation.Operation',
                                  on_delete=models.CASCADE)

    note = models.TextField(_('note'), null=True, blank=True, max_length=140)
