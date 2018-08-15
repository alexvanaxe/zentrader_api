from django.http.response import Http404
from rest_framework import viewsets, views, response


from operation.models import ExperienceData, BuyData, SellData
from operation.serializers import ExperienceDataSerializer, \
    BuyDataSerializer, SellDataSerializer


class ExperienceDataViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the ExperienceData.
    """
    queryset = ExperienceData.objects.filter(archived=False).order_by('-favorite', 'creation_date')
    serializer_class = ExperienceDataSerializer


class BuyDataViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the BuyData.
    """
    queryset = BuyData.objects.filter(archived=False).order_by('creation_date')
    serializer_class = BuyDataSerializer


class SellDataViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the SellData.
    """
    queryset = SellData.objects.filter(archived=False)
    serializer_class = SellDataSerializer
