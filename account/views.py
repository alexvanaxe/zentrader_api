from rest_framework import viewsets

from account.models import Account
from account.serializers import AccountSerializer


class AccountViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the account.
    """
    queryset = Account.objects.filter(next_account__isnull=True)
    serializer_class = AccountSerializer
