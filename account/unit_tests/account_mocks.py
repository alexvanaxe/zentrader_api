from account.models import Account


def create_account(cls):
    cls.account = Account.objects.create(broker="test", operation_cost=10, equity=10000)