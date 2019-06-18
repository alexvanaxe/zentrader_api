from django.test.testcases import TestCase
from django.core.cache import cache

from operation.models import SellData
from stock.unit_tests.stock_mocks import create_stocks
from account.unit_tests.account_mocks import create_account
from operation.unit_tests.operation_mocks import create_operations, create_day_trades, create_ir_operations, create_half_sell
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

class SellDataModelTest(OperationModelTestCase):
    def test_sell_fields(self):
        create_operations(self, self.stock, self.user)

        self.assertEqual("{0:.2f}".format(self.sell1.result()), "148.94")
        self.assertEqual("{0:.2f}".format(self.sell1.profit()), "185.98")
        self.assertEqual("{0:.2f}".format(self.sell1.profit_percent()), "20.51")
        self.assertEqual("{0:.2f}".format(self.sell1.sell_value()), "1092.64")
        self.assertEqual("{0:.2f}".format(self.sell1.gain_percent()), "14.97")

    def test_shark(self):
        create_operations(self, self.stock, self.user)
        self.assertEqual('-720.01', str(self.sell3.stop_loss_result()))
        self.assertEqual('1.01', str(SellData.solds.shark().shark))

    def test_amount(self):
        """
        Tests the amount available to sell based on the buy. The idea is
        totally chain the sell with the buy.
        """
        create_half_sell(self, self.stock, self.user)
        self.assertEqual(str(self.sell_hf1.amount_available(executed_filter=True)), '100')
