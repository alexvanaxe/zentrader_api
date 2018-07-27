from datetime import datetime

from django.test.testcases import TestCase
from django.core.exceptions import ValidationError

from operation.models import ExperienceData, BuyData
from account.models import Account
from stock.unit_tests.stock_mocks import create_stocks
from account.unit_tests.account_mocks import create_account, create_third_account
from operation.unit_tests.operation_mocks import create_operations, create_day_trades, create_ir_operations, create_super_buy



class OperationModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_account(cls)
        create_stocks(cls)


class OperationModelTest(OperationModelTestCase):
    def test_create(self):
        operation = ExperienceData.objects.create(stock=self.stock,
                                                  account=Account.objects.all()[0],
                                                  date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                  amount=1000, price=30)

        self.assertIsNotNone(operation.creation_date)

    def test_real_cost(self):
        operation = ExperienceData.objects.create(stock=self.stock,
                                                  account=Account.objects.all()[0],
                                                  date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                  amount=1000, price=30)

        self.assertEqual(str(operation.stock_cost()), '20000')
        self.assertEqual(str("{0:.2f}".format(operation.operation_average_price())), '30.02')

    def test_target_percent(self):
        operation = ExperienceData.objects.create(stock=self.stock,
                                                  account=Account.objects.all()[0],
                                                  date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                                  amount=1000, price=30,
                                                  target=35.34)

        self.assertEqual(str("{0:.2f}".format(operation.target_gain_percent())), '17.73')

    def test_gain_percent(self):
        operation = BuyData.objects.create(stock=self.stock,
                                           account=Account.objects.all()[0],
                                           date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                           amount=1000, price=30)

        self.assertEqual(str("{0:.2f}".format(operation.operation_gain_percent())), '-33.39')

    def test_is_day_trade(self):
        create_day_trades(self, self.stock)

        self.assertTrue(self.sell_dt1.is_daytrade())
        self.assertFalse(self.buy_dt1.is_daytrade())
        self.assertEqual(str("{0:.2f}".format(self.sell_dt1.result())), "23987.20")


    def test_is_day_trade_false(self):
        create_ir_operations(self, self.stock)

        self.assertFalse(self.sell1.is_daytrade())

class SellDataModelTest(OperationModelTestCase):
    def test_sell_result(self):
        create_operations(self, self.stock)

        self.assertEqual("{0:.2f}".format(self.sell1.result()), "148.94")

class BuyDataModelTest(OperationModelTestCase):
    def test_buy_not_alowed(self):
       create_third_account(self)
       with self.assertRaises(ValidationError):
           create_super_buy(self, self.stock, self.account3)


