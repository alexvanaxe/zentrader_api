from datetime import datetime

from operation.models import ExperienceData, BuyData, SellData
from account.models import Account


def create_operations(cls, stock):
    cls.operation = ExperienceData.objects.create(stock=stock,
                                                  account=Account.objects.all()[0],
                                                  date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                  amount=1000, price=30)

    cls.operation_archived = ExperienceData.objects.create(stock=stock,
                                                           account=Account.objects.all()[0],
                                                           date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=1000, price=20,
                                                           archived=True)

    cls.experience = ExperienceData.objects.create(stock=stock,
                                                   account=Account.objects.all()[0],
                                                   date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                   target=20, stop_loss=28,
                                                   amount=1000, price=30)

    cls.experience_archived = ExperienceData.objects.create(stock=stock,
                                                            account=Account.objects.all()[0],
                                                            date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                            amount=1000, price=20,
                                                            archived=True, stop_loss=20)


    cls.buy1 = BuyData.objects.create(stock=stock, account=Account.objects.all()[0],
                                                           date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=100, price=20)

    cls.buy2 = BuyData.objects.create(stock=stock, account=Account.objects.all()[0],
                                                           date=datetime.strptime('2017-06-13T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=150, price=18)

    cls.sell1 = SellData.objects.create(stock=stock, account=Account.objects.all()[0],
                                                           date=datetime.strptime('2017-06-18T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=50, price=22)

    cls.buy3 = BuyData.objects.create(stock=stock, account=Account.objects.all()[0],
                                                           date=datetime.strptime('2017-06-25T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=100, price=20)

    cls.sell2 = SellData.objects.create(stock=stock, account=Account.objects.all()[0],
                                                           date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=100, price=23)


def create_only_buy(cls, stock):
    cls.buy1 = BuyData.objects.create(stock=stock, account=Account.objects.all()[0],
                                      date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                      amount=100, price=20)


def create_ir_operations(cls, stock):
    cls.buy1 = BuyData.objects.create(stock=stock, account=Account.objects.all()[0],
                                      date=datetime.strptime('2017-06-01T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                      amount=1000, price=20)

    cls.buy2 = BuyData.objects.create(stock=stock, account=Account.objects.all()[0],
                                      date=datetime.strptime('2017-06-05T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                      amount=1500, price=18)

    cls.sell1 = SellData.objects.create(stock=stock, account=Account.objects.all()[0],
                                        date=datetime.strptime('2017-06-07T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                        amount=1500, price=30)


def create_day_trades(cls, stock):
    cls.buy_dt1 = BuyData.objects.create(stock=stock, account=Account.objects.all()[0],
                                         date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                         amount=1000, price=10)

    cls.sell_dt1 = SellData.objects.create(stock=stock, account=Account.objects.all()[0],
                                           date=datetime.strptime('2017-06-10T17:52:30', '%Y-%m-%dT%H:%M:%S'),
                                           amount=800, price=30)

def create_buys(cls, stock):
    cls.buy1 = BuyData.objects.create(stock=stock, account=Account.objects.all()[0],
                                                           date=datetime.strptime('2017-06-10T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=100, price=20)

def create_sells(cls, stock):
    cls.sell1 = SellData.objects.create(stock=stock, account=Account.objects.all()[0],
                                                           date=datetime.strptime('2017-06-18T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=100, price=22)
