from django.test.testcases import TestCase
from datetime import datetime
from django.core.cache import cache

from stock.unit_tests.stock_mocks import create_stocks
from account.unit_tests.account_mocks import create_account
from operation.unit_tests.operation_mocks import create_operations, create_only_buy
from zen_oauth.unit_tests.user_mocks import create_test_user, create_auth


class StockModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cache.clear()
        create_test_user(cls)
        create_auth(cls, cls.user)
        create_account(cls)
        create_stocks(cls)
        create_operations(cls, cls.stock, cls.user)


class StockTestCase(StockModelTestCase):
    def test_owned_margin(self):
        self.assertEqual(str(self.stock.owned(datetime.strptime('2017-06-10T15:52:30',
                                                                '%Y-%m-%dT%H:%M:%S'),
                                              datetime.strptime('2017-06-25T15:52:30',
                                                                '%Y-%m-%dT%H:%M:%S'))), str(300))

    def test_owned(self):
        self.assertEqual(str(self.stock.owned()), str(200))

    def test_average_price(self):
        self.assertEqual('{0:.2f}'.format(self.stock.average_price()), "19.28")


class StockEmptyTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_test_user(cls)
        create_auth(cls, cls.user)
        create_account(cls)
        create_stocks(cls)

    def tearDown(self):
        cache.clear()

    def test_owned_empty(self):
        self.assertEqual(str(self.stock.owned()), "0")

    def test_one_buy(self):
        create_only_buy(self, self.stock, self.user)
        self.assertEqual(str(self.stock.owned()), "100")
