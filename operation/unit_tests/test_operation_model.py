from django.test.testcases import TestCase
from django.core.cache import cache

from stock.unit_tests.stock_mocks import create_stocks
from account.unit_tests.account_mocks import create_account
from operation.unit_tests.operation_mocks import create_day_trades, create_ir_operations
from zen_oauth.unit_tests.user_mocks import create_test_user, create_auth


class OperationModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cache.clear()
        create_test_user(cls)
        create_auth(cls, cls.user)
        create_account(cls)
        create_stocks(cls)


class OperationModelTest(OperationModelTestCase):

    def test_is_day_trade(self):
        create_day_trades(self, self.stock, self.user)

        self.assertTrue(self.sell_dt1.is_daytrade())
        self.assertEqual(str("{0:.2f}".format(self.sell_dt1.result())),
                         "15976.60")

    def test_is_day_trade_false(self):
        create_ir_operations(self, self.stock, self.user)

        self.assertFalse(self.sell1.is_daytrade())
