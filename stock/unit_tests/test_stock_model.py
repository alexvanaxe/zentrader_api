from django.test.testcases import TestCase

from stock.unit_tests.stock_mocks import create_stocks
from account.unit_tests.account_mocks import create_account
from operation.unit_tests.operation_mocks import create_operations, create_only_buy


class StockModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_account(cls)
        create_stocks(cls)
        create_operations(cls, cls.stock)


class StockTestCase(StockModelTestCase):
    def test_owned(self):
        self.assertEqual(str(self.stock.owned()), str(200))

    def test_average_price(self):
        self.assertEqual('{0:.2f}'.format(self.stock.average_price()), "19.27")


class StockEmptyTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_account(cls)
        create_stocks(cls)

    def test_owned_empty(self):
        self.assertEqual(str(self.stock.owned()), "0")

    def test_one_buy(self):
        create_only_buy(self, self.stock)
        self.assertEqual(str(self.stock.owned()), "100")
