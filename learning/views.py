import rest_framework
import learning.models as models
import learning.serializers as serializers


# Create your views here.
class PaperBuyViewSet(rest_framework.viewsets.ModelViewSet):
    """
    A viewset representing the PaperBuy model.
    """
    queryset = models.PaperBuy.objects.all()

    serializer_class = serializers.PaperBuySerializer


class PaperSellViewSet(rest_framework.viewsets.ModelViewSet):
    """
    A viewset representing the PaperBuy model.
    """
    queryset = models.PaperSell.objects.all()

    serializer_class = serializers.PaperSellSerializer
