from django.test.testcases import TestCase
from django.core.cache import cache

from sell.models import SellData
from stock.unit_tests.stock_mocks import create_stocks
from account.unit_tests.account_mocks import create_account
from operation.unit_tests.operation_mocks import create_operations
from sell.unit_tests.sell_mocks import create_half_sell
from zen_oauth.unit_tests.user_mocks import create_test_user, create_auth


class OperationModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cache.clear()
        create_test_user(cls)
        create_auth(cls, cls.user)
        create_account(cls)
        create_stocks(cls)


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
        self.assertEqual('0.72', str(SellData.solds.shark().shark))

    def test_amount(self):
        """
        Tests the amount available to sell based on the buy. The idea is
        totally chain the sell with the buy.
        """
        create_half_sell(self, self.stock, self.user)
        self.assertEqual(str(self.sell_hf1.amount_available(executed_filter=True)), '100')
