import rest_framework
from trade_system.models import Analysis, Indicator, TechnicalAnalyze
from trade_system.serializers import AnalysisSerializer,\
                                     IndicatorSerializer,\
                                     TechnicalAnalyzeSerializer


class AnalysisViewSet(rest_framework.viewsets.ModelViewSet):
    """
    A viewset to serve the Analysis
    """
    queryset = Analysis.objects.all()

    serializer_class = AnalysisSerializer


class TechnicalAnalyzeViewSet(rest_framework.viewsets.ModelViewSet):
    """
    A viewset to serve the Technical Analyzes
    """
    queryset = TechnicalAnalyze.objects.all()

    serializer_class = TechnicalAnalyzeSerializer


class IndicatorViewSet(rest_framework.viewsets.ModelViewSet):
    """
    A viewset to serve the Indicators
    """
    queryset = Indicator.objects.all()

    serializer_class = IndicatorSerializer
