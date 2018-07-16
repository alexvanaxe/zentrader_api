from rest_framework import viewsets

from account.models import Account
from account.serializers import AccountSerializer


class AccountViewSet(viewsets.ModelViewSet):
    """
    A viewset representing the account.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
