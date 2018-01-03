from rest_framework import viewsets

from stock.models import Stock
from stock.serializers import StockSerializer


class StockViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the stock.
    """
    queryset = Stock.objects.all().order_by('code')
    serializer_class = StockSerializer

