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


class StockApiView(APIView):
    """
    APIView created for not generated (CRUD) functionalities of the stock.
    """
    def post(self, request, format=None):
        """ Updates automatically the stock """
        serializer = StockSerializer(data=request.data)

        if serializer.is_valid():
            stock_tmp = Stock(**serializer.validated_data)
            stock = Stock.objects.get(pk=request.data['pk'])
            stock.update_stock()

            serializer_updated = StockSerializer(stock)

            return Response(serializer_updated.data)
