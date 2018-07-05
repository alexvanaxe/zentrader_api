from account.models import Account


def create_account(cls):
    cls.account = Account.objects.create(broker="test", operation_cost=10, equity=10000)


def create_second_account(cls):
    if not cls.account:
        create_account(cls)

    cls.account2 = Account.objects.create(next_account=cls.account, broker="test", operation_cost=15, equity=10000)
