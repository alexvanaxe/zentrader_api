from datetime import datetime

from sell.models import SellData
from buy.models import BuyData
from account.models import Account


def create_sells(cls, stock, user):
    cls.sell1 = SellData.objects.create(stock=stock, owner=user, account=Account.objects.all()[0],
                                                           creation_date=datetime.strptime('2017-06-18T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           execution_date=datetime.strptime('2017-06-18T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=100, price=22, executed=True)


def create_half_sell(cls, stock, user):
    cls.buy_hf1 = BuyData.objects.create(stock=stock, owner=user, account=Account.objects.all()[0],
                                                           creation_date=datetime.strptime('2017-06-13T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           execution_date=datetime.strptime('2017-06-13T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=150, price=18, executed=True)

    cls.sell_hf1 = SellData.objects.create(stock=stock, owner=user, account=Account.objects.all()[0],
                                                           buy=cls.buy_hf1,
                                                           creation_date=datetime.strptime('2017-06-18T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           execution_date=datetime.strptime('2017-06-18T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=50, price=22, executed=True, stop_loss=17)

    cls.sell_hf3 = SellData.objects.create(stock=stock, owner=user, account=Account.objects.all()[0],
                               buy=cls.buy_hf1,
                               creation_date=datetime.strptime('2017-06-18T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                               amount=50, price=22, stop_loss=17)

    cls.buy_hf2 = BuyData.objects.create(stock=stock, owner=user, account=Account.objects.all()[0],
                                                           creation_date=datetime.strptime('2017-06-13T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           execution_date=datetime.strptime('2017-06-13T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=150, price=18, executed=True)

    cls.sell_hf2 = SellData.objects.create(stock=stock, owner=user, account=Account.objects.all()[0],
                               buy=cls.buy_hf2,
                               creation_date=datetime.strptime('2017-06-18T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                               execution_date=datetime.strptime('2017-06-18T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                               amount=50, price=22, executed=True, stop_loss=17)

    cls.buy_hf3 = BuyData.objects.create(stock=stock, owner=user, account=Account.objects.all()[0],
                                                           creation_date=datetime.strptime('2017-06-13T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           execution_date=datetime.strptime('2017-06-13T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                           amount=150, price=18, executed=True)
