from rest_framework import viewsets, views, response

from account.models import Account
from account.serializers import AccountSerializer


class AccountViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the account.
    """
    queryset = Account.objects.filter(next_account__isnull=True)
    serializer_class = AccountSerializer


class AccountDefault(views.APIView):
    """
    View to get the default account.
    """
    def get(self, request, format=None):
        serializer = AccountSerializer(Account.objects.filter(next_account__isnull=True)[0])
        return response.Response(serializer.data)

