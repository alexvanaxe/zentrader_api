from rest_framework import viewsets, views, response

from operation.models import Operation, SellData
from operation.serializers import SellDataSerializer, RiskDataSerializer, ArchiveSerializer


class SellDataViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the SellData.
    """
    queryset = SellData.objects.filter(archived=False).order_by('-favorite',
                                                                'creation_date')
    serializer_class = SellDataSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

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
