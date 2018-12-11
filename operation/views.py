from django.http.response import Http404
from rest_framework import viewsets, views, response


from operation.models import Operation, ExperienceData, BuyData, SellData
from operation.serializers import ExperienceDataSerializer, \
    BuyDataSerializer, SellDataSerializer, RiskDataSerializer, \
    ArchiveSerializer


class ExperienceDataViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the ExperienceData.
    """
    queryset = ExperienceData.objects.filter(archived=False).order_by('-favorite', 'creation_date')
    serializer_class = ExperienceDataSerializer


class BuyDataViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the BuyData.
    """
    queryset = BuyData.objects.filter(archived=False).order_by('creation_date')
    serializer_class = BuyDataSerializer


class SellDataViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the SellData.
    """
    queryset = SellData.objects.filter(archived=False).order_by('archived', 'creation_date')
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
