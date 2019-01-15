from rest_framework import viewsets, views, response, mixins
from silk.profiling.profiler import silk_profile


from operation.models import Operation, ExperienceData, BuyData, SellData
from operation.serializers import ExperienceDataSerializer, ExperienceDataSerializerDetailed, \
    BuyDataSerializer, SellDataSerializer, RiskDataSerializer, \
    ArchiveSerializer


class ExperienceDataViewSet(mixins.CreateModelMixin,
                            mixins.ListModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            viewsets.GenericViewSet):
    """
    A viewset representing the ExperienceData.
    """
    queryset = ExperienceData.objects.filter(archived=False).order_by('-favorite',
                                                                      'creation_date')
    serializer_class = ExperienceDataSerializer

    @silk_profile(name="Experience data list")
    def list(self, request, *args, **kwargs):
        """ Override to serialize the full experience when the detailed attribute
            is sended true
        """
        queryset = ExperienceData.objects.filter(archived=False).order_by('-favorite',
                                                                          'creation_date')
        try:
            detailed = request.query_params['detailed'].lower()
        except KeyError:
            detailed = 'false'

        if detailed == 'true':
            return response.Response(ExperienceDataSerializerDetailed(queryset, many=True).data)
        else:
            return response.Response(ExperienceDataSerializer(queryset, many=True).data)

    @silk_profile(name="Experience data retrieve")
    def retrieve(self, request, pk, *args, **kwargs):
        """ Override to serialize the full experience when the detailed querystring is set to true"""

        try:
            detailed = request.query_params['detailed'].lower()
        except KeyError:
            detailed = 'false'

        if detailed == 'true':
            return response.Response(ExperienceDataSerializerDetailed(ExperienceData.objects.get(pk=pk)).data)
        else:
            return response.Response(ExperienceDataSerializer(ExperienceData.objects.get(pk=pk)).data)


class BuyDataViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the BuyData.
    """
    queryset = BuyData.objects.filter(archived=False).order_by('-favorite',
                                                               'creation_date')
    serializer_class = BuyDataSerializer


class SellDataViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the SellData.
    """
    queryset = SellData.objects.filter(archived=False).order_by('-favorite',
                                                                'creation_date')
    serializer_class = SellDataSerializer


class RiskDataApiView(views.APIView):
    """
    View to get the risk, it returns the shark for the current buy
    """
    def get(self, request, format=None):
        serializer = RiskDataSerializer(SellData.solds.shark())
        return response.Response(serializer.data)


class ArchiveApiView(views.APIView):
    def patch(self, request, pk, format=None):
        instance = Operation.objects.get(pk=pk)
        serializer = ArchiveSerializer(instance)
        serializer.save(instance)

        return response.Response(serializer.data)
