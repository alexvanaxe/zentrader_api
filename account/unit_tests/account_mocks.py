from account.models import Account


def create_account(cls):
    cls.account = Account.objects.create(broker="test", operation_cost_day_trade=5, operation_cost_fraction=7,
                                         operation_cost_position=10, equity=10000)


def create_second_account(cls):
    if not cls.account:
        create_account(cls)

    cls.account2 = Account.objects.create(next_account=cls.account, broker="test", operation_cost_position=15,
                                          operation_cost_day_trade=10, operation_cost_fraction=6, equity=10000)
