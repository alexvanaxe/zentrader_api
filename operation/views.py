from rest_framework import viewsets, views, response, mixins


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
    serializer_class = ExperienceDataSerializerDetailed

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

    def get_queryset(self):
        """
        Optionaly restrict the bought returned from a specific experience
        passed as in the querystring with the key experience.
        """
        queryset = BuyData.objects.filter(archived=False).order_by('-favorite',
                                                                   'creation_date')

        experience_pk = self.request.query_params.get('experience', None)

        if experience_pk:
            queryset = queryset.filter(experience=experience_pk)

        return queryset


class SellDataViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the SellData.
    """
    queryset = SellData.objects.filter(archived=False).order_by('-favorite',
                                                                'creation_date')
    serializer_class = SellDataSerializer

    def get_queryset(self):
        queryset = SellData.objects.filter(archived=False).order_by('-favorite',
                                                                    'creation_date')

        buy_pk = self.request.query_params.get('buy', None)

        if buy_pk:
            queryset = queryset.filter(buy=buy_pk)

        return queryset


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
