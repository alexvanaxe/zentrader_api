from account.models import Account


def create_account(cls):
    cls.account = Account.objects.create(broker="test", operation_cost_day_trade=5,
                                         operation_cost_fraction=7,
                                         operation_cost_position=10,
                                         equity=100000)

def create_zero_account(cls):
    cls.account_zero = Account.objects.create(broker="test", operation_cost_day_trade=0,
                                         operation_cost_fraction=0,
                                         operation_cost_position=0,
                                         equity=100000)


def create_second_account(cls):
    if not cls.account:
        create_account(cls)


    cls.account2 = Account.objects.create(broker="test",
                                          operation_cost_position=15,
                                          operation_cost_day_trade=10,
                                          operation_cost_fraction=6, equity=100000)


    cls.account.next_account = cls.account2
    cls.account.save()


def create_third_account(cls):
    cls.account3 = Account.objects.create(broker="test2",
                                          operation_cost_position=15,
                                          operation_cost_day_trade=10,
                                          operation_cost_fraction=6, equity=10000)
