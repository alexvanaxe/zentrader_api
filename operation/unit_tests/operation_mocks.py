from datetime import datetime

from operation.models import ExperienceData, BuyData, SellData
from account.models import Account


def create_operations(cls, stock):
    cls.operation = ExperienceData.objects.create(stock=stock,
                                                  account=Account.objects.all()[0],
                                                  creation_date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                  amount=1000, price=30)

    cls.operation_archived = ExperienceData.objects.create(stock=stock,
                                                           account=Account.objects.all()[0],
                                                           creation_date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=1000, price=20,
                                                           archived=True)

    cls.experience = ExperienceData.objects.create(stock=stock,
                                                   account=Account.objects.all()[0],
                                                   creation_date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                   target=20, stop_loss=28,
                                                   amount=1000, price=30)

    cls.experience_archived = ExperienceData.objects.create(stock=stock,
                                                            account=Account.objects.all()[0],
                                                            creation_date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                            amount=1000, price=20,
                                                            archived=True)

    cls.buy1 = BuyData.objects.create(stock=stock, account=Account.objects.all()[0],
                                                           creation_date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           execution_date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=100, price=20, executed=True)

    cls.buy2 = BuyData.objects.create(stock=stock, account=Account.objects.all()[0],
                                                           creation_date=datetime.strptime('2017-06-13T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           execution_date=datetime.strptime('2017-06-13T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=150, price=18, executed=True)

    cls.sell1 = SellData.objects.create(stock=stock, account=Account.objects.all()[0],
                                                           buy=cls.buy2,
                                                           creation_date=datetime.strptime('2017-06-18T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           execution_date=datetime.strptime('2017-06-18T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=50, price=22, executed=True, stop_loss=17)

    cls.buy3 = BuyData.objects.create(stock=stock, account=Account.objects.all()[0],
                                                           creation_date=datetime.strptime('2017-06-25T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           execution_date=datetime.strptime('2017-06-25T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=100, price=20, executed=True)

    cls.sell2 = SellData.objects.create(stock=stock, account=Account.objects.all()[0],
                                                           buy=cls.buy2,
                                                           creation_date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           execution_date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=100, price=23, stop_loss=21.50, executed=True)

    cls.sell3 = SellData.objects.create(stock=stock, account=Account.objects.all()[0],
                                        buy=cls.buy3,
                                        creation_date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                        execution_date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                        amount=100,
                                        price=23, stop_loss=13)

def create_only_buy(cls, stock):
    cls.buy1 = BuyData.objects.create(stock=stock, account=Account.objects.all()[0],
                                      creation_date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                      execution_date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                      amount=100, price=20, executed=True)


def create_ir_operations(cls, stock):
    cls.buy1 = BuyData.objects.create(stock=stock, account=Account.objects.all()[0],
                                      creation_date=datetime.strptime('2017-06-01T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                      execution_date=datetime.strptime('2017-06-01T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                      amount=1000, price=20, executed=True)

    cls.buy2 = BuyData.objects.create(stock=stock, account=Account.objects.all()[0],
                                      creation_date=datetime.strptime('2017-06-05T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                      execution_date=datetime.strptime('2017-06-05T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                      amount=1500, price=18, executed=True)

    cls.sell1 = SellData.objects.create(stock=stock, account=Account.objects.all()[0],
                                        creation_date=datetime.strptime('2017-06-07T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                        execution_date=datetime.strptime('2017-06-07T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                        amount=1500, price=30, executed=True)


def create_day_trades(cls, stock):
    cls.buy_dt1 = BuyData.objects.create(stock=stock, account=Account.objects.all()[0],
                                         creation_date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                         execution_date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                         amount=1000, price=10, executed=True)

    cls.sell_dt1 = SellData.objects.create(stock=stock, account=Account.objects.all()[0],
                                           creation_date=datetime.strptime('2017-06-10T17:52:30', '%Y-%m-%dT%H:%M:%S'),
                                           execution_date=datetime.strptime('2017-06-10T17:52:30', '%Y-%m-%dT%H:%M:%S'),
                                           amount=800, price=30, executed=True)

def create_buys(cls, stock):
    cls.buy1 = BuyData.objects.create(stock=stock, account=Account.objects.all()[0],
                                                           creation_date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           execution_date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=100, price=20, executed=True)

def create_sells(cls, stock):
    cls.sell1 = SellData.objects.create(stock=stock, account=Account.objects.all()[0],
                                                           creation_date=datetime.strptime('2017-06-18T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           execution_date=datetime.strptime('2017-06-18T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=100, price=22, executed=True)

def create_super_buy(cls, stock, account):
    cls.super_buy = BuyData.objects.create(stock=stock, account=account,
                                      creation_date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                      execution_date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                      amount=10000, price=200, executed=True)
