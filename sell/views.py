from rest_framework import viewsets, views, response
from rest_framework.pagination import PageNumberPagination, Response
from django_filters.rest_framework import DjangoFilterBackend
from collections import OrderedDict

from sell.serializers import SellDataSerializer, RiskDataSerializer
from sell.models import SellData


class StandardResultsSetPagination(PageNumberPagination):
    """
    Class to configure the pagination.
    """
    page_size = 2
    page_size_query_param = 'page_size'
    max_page_size = 2

    def get_paginated_response(self, data):
        return Response(OrderedDict([
             ('lastPage', self.page.paginator.count),
             ('countItemsOnPage', self.page_size),
             ('current', self.page.number),
             ('next', self.get_next_link()),
             ('previous', self.get_previous_link()),
             ('results', data)
         ]))


class RiskDataApiView(views.APIView):
    """
    View to get the risk, it returns the shark for the current buy
    """
    def get(self, request, format=None):
        serializer = RiskDataSerializer(SellData.solds.shark())
        return response.Response(serializer.data)


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


class SellPaginatedDataViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the BuyData.
    """
    queryset = SellData.objects.all().order_by('archived', '-favorite', 'creation_date')
    serializer_class = SellDataSerializer

    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('archived', 'buy')

    pagination_class = StandardResultsSetPagination

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
