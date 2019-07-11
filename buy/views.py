from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend

from buy.models import BuyData
from buy.serializers import BuyDataSerializer


class StandardResultsSetPagination(PageNumberPagination):
    """
    Class to configure the pagination.
    """
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 2


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


class BuyPaginatedDataViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the BuyData.
    """
    queryset = BuyData.objects.all().order_by('archived', '-favorite', 'creation_date')
    serializer_class = BuyDataSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('archived', 'experience')

    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
