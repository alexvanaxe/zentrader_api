from django.db import models
from django.utils.translation import ugettext_lazy as _


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

    beginning = models.DecimalField(_('beginning'), max_digits=22,
                                    decimal_places=2,
                                    null=True, blank=True)

    end = models.DecimalField(_('end'), max_digits=22, decimal_places=2,
                              null=True, blank=True)

    def technical_analyze_data(self):
        return self.indicators.all()[0].technicalanalyze_set.\
                                        filter(analysis=self)
