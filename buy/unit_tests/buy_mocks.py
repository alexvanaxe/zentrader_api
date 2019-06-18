from datetime import datetime

from buy.models import BuyData
from account.models import Account


def create_only_buy(cls, stock, user):
    cls.buy1 = BuyData.objects.create(stock=stock, owner=user, account=Account.objects.all()[0],
                                      creation_date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                      execution_date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                      amount=100, price=20, executed=True)


def create_buys(cls, stock, user):
    cls.buy1 = BuyData.objects.create(stock=stock, owner=user, account=Account.objects.all()[0],
                                                           creation_date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           execution_date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=100, price=20, executed=True)

    cls.buy2 = BuyData.objects.create(stock=stock, owner=user, account=Account.objects.all()[0],
                                                           creation_date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           execution_date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=200, price=20, executed=True)

def create_super_buy(cls, stock, account, user):
    cls.super_buy = BuyData.objects.create(stock=stock, owner=user, account=account,
                                      creation_date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                      execution_date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                      amount=10000, price=200, executed=True)
