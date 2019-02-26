from decimal import Decimal

from django.test.testcases import TestCase
from django.core.exceptions import ValidationError
from django.core.cache import cache

from operation.models import ExperienceData, BuyData, SellData
from account.models import Account
from stock.unit_tests.stock_mocks import create_stocks
from account.unit_tests.account_mocks import create_account, create_third_account
from operation.unit_tests.operation_mocks import create_operations, create_day_trades, create_ir_operations, create_super_buy, create_half_sell
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
    def test_create(self):
        operation = ExperienceData.objects.create(stock=self.stock,
                                                  owner=self.user,
                                                  account=Account.objects.all()[0],
                                                  amount=1000, price=30)

        self.assertIsNotNone(operation.creation_date)

    def test_real_cost(self):
        operation = ExperienceData.objects.create(stock=self.stock,
                                                  owner=self.user,
                                                  account=Account.objects.all()[0],
                                                  amount=1000, price=30)

        self.assertEqual(str(operation.stock_cost()), '20000')
        self.assertEqual(str("{0:.2f}".format(operation.operation_average_price())), '30.02')

    def test_target_percent(self):
        operation = ExperienceData.objects.create(stock=self.stock,
                                                  owner=self.user,
                                                  account=Account.objects.all()[0],
                                                  amount=1000, price=30,
                                                  target=Decimal("35.34"))

        self.assertEqual(str("{0:.2f}".format(operation.target_gain_percent())), '17.73')

    def test_gain_percent(self):
        operation = BuyData.objects.create(stock=self.stock,
                                           owner=self.user,
                                           account=Account.objects.all()[0],
                                           amount=1000, price=30)

        self.assertEqual(str("{0:.2f}".format(operation.operation_gain_percent())), '-33.39')

    def test_is_day_trade(self):
        create_day_trades(self, self.stock, self.user)

        self.assertTrue(self.sell_dt1.is_daytrade())
        self.assertFalse(self.buy_dt1.is_daytrade())
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
        self.assertEqual(str(self.buy_hf3.amount_available(executed_filter=True)), '150')


class BuyDataModelTest(OperationModelTestCase):
    def test_buy_not_alowed(self):
       create_third_account(self)
       with self.assertRaises(ValidationError):
           create_super_buy(self, self.stock, self.account3, self.user)
           self.super_buy.clean()

    def test_remaining_gain(self):
        create_operations(self, self.stock, self.user)
        self.assertEqual("1989.35", "{0:.2f}".format(self.buy3.remaining_gain()))
        self.assertEqual("0.00", "{0:.2f}".format(self.buy2.remaining_gain()))


class ExperimentDataModelTest(OperationModelTestCase):
    def test_experiment_default(self):
        create_operations(self, self.stock, self.user)
        self.assertEqual('None', str(self.operation.target_gain_percent()))

    def test_total_percentage_experiment(self):
        create_operations(self, self.stock, self.user)
        experience = ExperienceData.objects.get(pk=self.operation.pk)
        self.assertEqual('-9.96', "{0:.2f}".format(experience.experience_total_gain_percent()))
