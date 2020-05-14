from datetime import datetime

from sell.models import  SellData
from buy.models import BuyData
from account.models import Account

from experience.unit_tests.experience_mocks import create_experiences

def create_operations(cls, stock, user):
    create_experiences(cls, stock, user)

    cls.buy1 = BuyData.objects.create(stock=stock, owner=user, experience=cls.experience, account=Account.objects.all()[0],
                                                           creation_date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           execution_date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=100, price=20, executed=True)

    cls.buy2 = BuyData.objects.create(stock=stock, owner=user, account=Account.objects.all()[0],
                                                           creation_date=datetime.strptime('2017-06-13T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           execution_date=datetime.strptime('2017-06-13T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=150, price=18, executed=True)

    cls.sell1 = SellData.objects.create(stock=stock, owner=user, account=Account.objects.all()[0],
                                                           buy=cls.buy2,
                                                           creation_date=datetime.strptime('2017-06-18T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           execution_date=datetime.strptime('2017-06-18T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=50, price=22, executed=True, stop_loss=17)

    cls.buy3 = BuyData.objects.create(stock=stock, owner=user, account=Account.objects.all()[0],
                                                           creation_date=datetime.strptime('2017-06-25T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           execution_date=datetime.strptime('2017-06-25T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=100, price=20, executed=True)

    cls.sell2 = SellData.objects.create(stock=stock, owner=user, account=Account.objects.all()[0],
                                                           buy=cls.buy2,
                                                           creation_date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           execution_date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=100, price=23, stop_loss=21.50, executed=True)

    cls.sell3 = SellData.objects.create(stock=stock, owner=user, account=Account.objects.all()[0],
                                        buy=cls.buy3,
                                        creation_date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                        execution_date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                        amount=100,
                                        price=23, stop_loss=13)


def create_recent_sells(cls, stock, user):
    create_experiences(cls, stock, user)

    cls.buy1 = BuyData.objects.create(stock=stock, owner=user, experience=cls.experience, account=Account.objects.all()[0],
                                                           creation_date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=100, price=20, executed=True)

    cls.buy2 = BuyData.objects.create(stock=stock, owner=user, account=Account.objects.all()[0],
                                                           creation_date=datetime.strptime('2017-06-13T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=150, price=18, executed=True)

    cls.sell1 = SellData.objects.create(stock=stock, owner=user, account=Account.objects.all()[0],
                                                           buy=cls.buy2,
                                                           creation_date=datetime.strptime('2017-06-18T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=50, price=22, executed=True, stop_loss=17)

    cls.buy3 = BuyData.objects.create(stock=stock, owner=user, account=Account.objects.all()[0],
                                                           creation_date=datetime.strptime('2017-06-25T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=100, price=20, executed=True)

    cls.sell2 = SellData.objects.create(stock=stock, owner=user, account=Account.objects.all()[0],
                                                           buy=cls.buy2,
                                                           creation_date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=100, price=23, stop_loss=21.50, executed=True)

    cls.sell3 = SellData.objects.create(stock=stock, owner=user, account=Account.objects.all()[0],
                                        buy=cls.buy3,
                                        creation_date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                        amount=100,
                                        price=23, stop_loss=13)



def create_ir_operations(cls, stock, user):
    cls.buy1 = BuyData.objects.create(stock=stock, owner=user, account=Account.objects.all()[0],
                                      creation_date=datetime.strptime('2017-06-01T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                      execution_date=datetime.strptime('2017-06-01T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                      amount=1000, price=20, executed=True)

    cls.buy2 = BuyData.objects.create(stock=stock, owner=user, account=Account.objects.all()[0],
                                      creation_date=datetime.strptime('2017-06-05T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                      execution_date=datetime.strptime('2017-06-05T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                      amount=1500, price=18, executed=True)

    cls.sell1 = SellData.objects.create(stock=stock, owner=user, account=Account.objects.all()[0], buy=cls.buy2,
                                        creation_date=datetime.strptime('2017-06-07T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                        execution_date=datetime.strptime('2017-06-07T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                        amount=1500, price=30, executed=True)


def create_day_trades(cls, stock, user):
    cls.buy_dt1 = BuyData.objects.create(stock=stock, owner=user, account=Account.objects.all()[0],
                                         creation_date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                         execution_date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                         amount=1000, price=10, executed=True)

    cls.sell_dt1 = SellData.objects.create(stock=stock, owner=user, account=Account.objects.all()[0], buy=cls.buy_dt1,
                                           creation_date=datetime.strptime('2017-06-10T17:52:31', '%Y-%m-%dT%H:%M:%S'),
                                           execution_date=datetime.strptime('2017-06-10T17:52:31', '%Y-%m-%dT%H:%M:%S'),
                                           amount=800, price=30, executed=True)
