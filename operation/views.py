from django.http.response import Http404
from rest_framework import viewsets, views, response


from operation.models import Operation, ExperienceData, OperationType, BuyData, SellData
from operation.serializers import OperationSerializer, ExperienceDataSerializer, OperationTypeSerializer, \
    OperationCostSerializer, BuyDataSerializer, SellDataSerializer, OperationNestedSerializer, \
    ExperienceDataNSerializer, BuyDataNSerializer, SellDataNSerializer


class ExperienceDataViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the ExperienceData.
    """
    queryset = ExperienceData.objects.filter(operation__archived=False)
    serializer_class = ExperienceDataSerializer


class ExperienceDataNViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset representing the ExperienceData.
    """
    queryset = ExperienceData.objects.filter(operation__archived=False).order_by('pk')
    serializer_class = ExperienceDataNSerializer


class BuyDataViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the BuyData.
    """
    queryset = BuyData.objects.filter(operation__archived=False)
    serializer_class = BuyDataSerializer


class BuyDataNViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset representing the Nested BuyData (readonly).
    """
    queryset = BuyData.objects.filter(operation__archived=False)
    serializer_class = BuyDataNSerializer


class SellDataViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the SellData.
    """
    queryset = SellData.objects.filter(operation__archived=False)
    serializer_class = SellDataSerializer


class SellDataNViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset representing the SellData.
    """
    queryset = SellData.objects.filter(operation__archived=False)
    serializer_class = SellDataNSerializer


class OperationViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the Operation.
    """
    queryset = Operation.objects.filter(archived=False)
    serializer_class = OperationSerializer


class ROOperationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A read only viewset, it provides only access to the read methods (get and list), but returns the nested attributes.
    """
    queryset = Operation.objects.filter(archived=False)
    serializer_class = OperationNestedSerializer

class OperationTypeViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the OperationType.
    """
    queryset = OperationType.objects.all()
    serializer_class = OperationTypeSerializer


class OperationCostView(views.APIView):
    def get_object(self, pk):
        try:
            return Operation.objects.get(pk=pk)
        except(Operation.DoesNotExist):
            raise Http404

    def get(self, request, pk, format=None):
        operation = self.get_object(pk)
        serializer = OperationCostSerializer(operation)
        return response.Response(serializer.data)
