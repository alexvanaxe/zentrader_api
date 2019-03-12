from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from stock.models import Stock
from stock.serializers import StockSerializer, OwnedStocksSerializer

def filter_stock(stock):
    return stock.owned() > 0

class StockViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the stock.
    """
    queryset = Stock.objects.all().order_by('code')
    serializer_class = StockSerializer

class OwnedStocksAPIView(APIView):

    def get(self, request, format=None):
        stock = Stock.resume.all()
        serializer = OwnedStocksSerializer((stock), many=True)

        return Response(serializer.data)


class OwnedByUserStocksAPIView(APIView):

    def get(self, request, format=None):
        stock = Stock.resume.filter(self.request.user)
        serializer = OwnedStocksSerializer((stock), many=True)

        return Response(serializer.data)
