from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend

from buy.models import BuyData
from buy.serializers import BuyDataSerializer


class BuyDataViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the BuyData.
    """
    queryset = BuyData.objects.all().order_by('archived', '-favorite', 'creation_date')
    serializer_class = BuyDataSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('archived', 'experience')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
