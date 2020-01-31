from django.db.models import Sum, F, Q
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from stock.models import Stock
from stock.serializers import StockSerializer, OwnedStocksSerializer

def filter_stock(stock):
    return stock.owned() > 0

def get_stock_queryset():
    return Stock.objects.filter(Q(operation__executed=True) | Q(operation__experiencedata__isnull=False) | Q(operation__isnull=True)).annotate(operations_s=Sum(F('operation__selldata__amount'))).annotate(operations_b=Sum(F('operation__buydata__amount'))).annotate(operations_t=F('operations_b') - F('operations_s'))


class StockViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the stock.
    """
    queryset = get_stock_queryset().order_by('code')
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
    def put(self, request, pk, format=None):
        """ Updates automatically the stock """
        stock = Stock.objects.get(pk=pk)
        stock.update_stock()

        serializer_updated = StockSerializer(stock)

        return Response(serializer_updated.data)
