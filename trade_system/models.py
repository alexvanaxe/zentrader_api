from decimal import Decimal, ROUND_DOWN
from datetime import datetime
from django.db import models
from django.utils.translation import gettext_lazy as _

from formulas import support_system_formulas


class Indicator(models.Model):
    """
    Indicators are tools used in technical analysis to support a decision.
    It can be oscillators, trend followers.
    It contains a name, and a kind.
    """
    name = models.CharField(_('name'), max_length=140)
    description = models.TextField(_('description'))
    indicator_kind = models.CharField(_('indicator kind'), max_length=140)

    def __str__(self):
        return self.name


class TechnicalAnalyze(models.Model):
    """
    Association between Indicator and Analysis.
    """
    indicator = models.ForeignKey('trade_system.Indicator', null=False,
                                  on_delete=models.CASCADE)
    analysis = models.ForeignKey('trade_system.Analysis', null=True,
                                 on_delete=models.CASCADE)
    comment = models.TextField(_('comment'))

    creation_date = models.DateTimeField(_('creation date'), null=False,
                                         editable=False)

    def save(self, *args, **kwargs):
        if not self.creation_date:
            self.creation_date = datetime.now()

        super().save(*args, **kwargs)

    def indicator_data(self):
        """
        Return the indicator details.
        """
        return self.indicator


class Analysis(models.Model):
    """
    An analysis of a position. It has five indicators with comments and a
    grade.
    """
    indicators = models.ManyToManyField('trade_system.Indicator',
                                        through='TechnicalAnalyze')

    tunnel_bottom = models.DecimalField(_('Bottom tunnel'), max_digits=22,
                                        decimal_places=2, null=True,
                                        blank=True)
    tunnel_top = models.DecimalField(_('Top tunnel'), max_digits=22,
                                     decimal_places=2, null=True, blank=True)

    def technical_analyze_data(self):
        return self.technicalanalyze_set.all().order_by('-pk')

    def grade(self):
        gain = self.operation.gain_per_stock()
        try:
            return Decimal(support_system_formulas.calculate_grade(gain,
                                                                   self.tunnel_top,
                                                                   self.tunnel_bottom))
        except(TypeError):
            return None

    def grade_symbol(self):
        return support_system_formulas.calculate_grade_symbol(self.grade())
