from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination, Response
from django_filters.rest_framework import DjangoFilterBackend
from collections import OrderedDict

from buy.models import BuyData
from buy.serializers import BuyDataSerializer


class StandardResultsSetPagination(PageNumberPagination):
    """
    Class to configure the pagination.
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10

    def get_paginated_response(self, data):
        return Response(OrderedDict([
             ('lastPage', self.page.paginator.count),
             ('countItemsOnPage', self.page_size),
             ('current', self.page.number),
             ('next', self.get_next_link()),
             ('previous', self.get_previous_link()),
             ('results', data)
         ]))


class BuyDataViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the BuyData.
    """
    queryset = BuyData.objects.all().order_by('archived', '-favorite',
                                              'creation_date')
    serializer_class = BuyDataSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('archived', 'experience')

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BuyPaginatedDataViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the BuyData.
    """
    queryset = BuyData.objects.all().order_by('archived', '-favorite',
                                              'creation_date')
    serializer_class = BuyDataSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('archived', 'experience')

    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
