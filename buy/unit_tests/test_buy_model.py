from django.test.testcases import TestCase
from django.core.exceptions import ValidationError
from django.core.cache import cache

from buy.models import BuyData
from account.models import Account
from stock.unit_tests.stock_mocks import create_stocks
from account.unit_tests.account_mocks import create_account, create_third_account
from operation.unit_tests.operation_mocks import create_operations, create_day_trades
from buy.unit_tests.buy_mocks import create_super_buy
from zen_oauth.unit_tests.user_mocks import create_test_user, create_auth


class BuyModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cache.clear()
        create_test_user(cls)
        create_auth(cls, cls.user)
        create_account(cls)
        create_stocks(cls)


class BuyModelTest(BuyModelTestCase):
    def test_gain_percent(self):
        operation = BuyData.objects.create(stock=self.stock,
                                           owner=self.user,
                                           account=Account.objects.all()[0],
                                           amount=1000, price=30)

        self.assertEqual(str("{0:.2f}".format(operation.operation_gain_percent())), '-33.39')

    def test_if_buy_is_day_trade(self):
        create_day_trades(self, self.stock, self.user)

        self.assertFalse(self.buy_dt1.is_daytrade())


class BuyDataModelTest(BuyModelTestCase):
    def test_buy_not_alowed(self):
       create_third_account(self)
       with self.assertRaises(ValidationError):
           create_super_buy(self, self.stock, self.account3, self.user)
           self.super_buy.clean()

    def test_remaining_gain(self):
        create_operations(self, self.stock, self.user)
        self.assertEqual("1989.35", "{0:.2f}".format(self.buy3.remaining_gain()))
        self.assertEqual("0.00", "{0:.2f}".format(self.buy2.remaining_gain()))

