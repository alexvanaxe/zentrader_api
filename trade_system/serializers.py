"""
Allow the complex data from the model instance of the account to be converted
to native Python datatypes, that can then be easily rendered into JSON, XML
or other content types.
Also provide deserialization, allowing parsed data to be converted back into
complex types, after first validating the incoming data.
"""

from rest_framework import serializers
from trade_system.models import TechnicalAnalyze, Indicator,\
                               Analysis


class IndicatorSerializer(serializers.ModelSerializer):
    """
    Serializer for Indicator.
    """
    class Meta:
        fields = ('pk', 'name', 'description', 'indicator_kind')
        model = Indicator


class TechnicalAnalyzeSerializer(serializers.ModelSerializer):
    """
    Serializer for TechnicalAnalyze.
    """
    indicator_data = IndicatorSerializer(read_only=True)

    class Meta:
        fields = ('pk', 'indicator', 'analysis', 'comment', 'indicator_data',
                  'creation_date')
        read_only_fields = ('indicator_data', 'creation_date')
        model = TechnicalAnalyze


class AnalysisSerializer(serializers.ModelSerializer):
    """
    Serializer for Analysis.
    """
    technical_analyze_data = TechnicalAnalyzeSerializer(read_only=True,
                                                        many=True)

    class Meta:
        fields = ('pk', 'indicators', 'technical_analyze_data', "tunnel_top",
                  "tunnel_bottom")
        read_only_fields = ('technical_analyze_data',)
        model = Analysis
