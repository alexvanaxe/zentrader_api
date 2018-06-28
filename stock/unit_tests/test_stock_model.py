from django.test.testcases import TestCase

from stock.unit_tests.stock_mocks import create_stocks
from account.unit_tests.account_mocks import create_account
from operation.unit_tests.operation_mocks import create_operations


class StockModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_account(cls)
        create_stocks(cls)
        create_operations(cls, cls.stock)


class StockTestCase(StockModelTestCase):
    def test_owned(self):
        self.assertEqual(str(self.stock.owned()), str(200))


class StockEmptyTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_account(cls)
        create_stocks(cls)

    def test_owned_empty(self):
        self.assertEqual(str(self.stock.owned()), str(0))
