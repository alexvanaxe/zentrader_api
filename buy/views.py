from rest_framework import viewsets

from operation.models import BuyData
from operation.serializers import BuyDataSerializer


class BuyDataViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the BuyData.
    """
    queryset = BuyData.objects.filter(archived=False).order_by('-favorite',
                                                               'creation_date')
    serializer_class = BuyDataSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        """
        Optionaly restrict the bought returned from a specific experience
        passed as in the querystring with the key experience.
        """
        queryset = BuyData.objects.filter(archived=False).order_by('-favorite',
                                                                   'creation_date')

        experience_pk = self.request.query_params.get('experience', None)

        if experience_pk:
            queryset = queryset.filter(experience=experience_pk)

        return queryset

