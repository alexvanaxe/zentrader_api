from rest_framework import viewsets, response, mixins, generics

from experience.models import ExperienceData
from experience.serializers import ExperienceDataSerializer, ExperienceDataSerializerDetailed


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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ExperienceListByStock(generics.ListAPIView):
    """
    Return the list of all experience operations filtered by a stock.
    """
    serializer_class = ExperienceDataSerializerDetailed

    def get_queryset(self):
        """
        Return a queryset containg all non archived experience of the stock.
        """
        stock_pk = self.kwargs['stock_pk']
        return ExperienceData.objects.filter(archived=False, stock=stock_pk)
