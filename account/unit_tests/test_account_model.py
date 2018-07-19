from datetime import datetime
from django.test.testcases import TestCase

from operation.models import ExperienceData
from account.unit_tests.account_mocks import create_account, create_second_account
from stock.unit_tests.stock_mocks import create_stocks
from operation.unit_tests.operation_mocks import create_buys, create_sells


class AccountModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_account(cls)
        create_stocks(cls)


class AccountModelTest(AccountModelTestCase):
    def test_create_account(self):
        operation = ExperienceData.objects.create(stock=self.stock,
                                                  date=datetime.strptime('2017-06-30T15:52:30',
                                                                         '%Y-%m-%dT%H:%M:%S'),
                                                  amount=1000, price=30)

        self.assertEqual(str(operation.account.operation_cost_position), "10.00")
        create_second_account(self)
        operation = ExperienceData.objects.create(stock=self.stock,
                                                  date=datetime.strptime('2017-06-30T15:52:30',
                                                                         '%Y-%m-%dT%H:%M:%S'),
                                                  amount=1000, price=30)

        self.assertEqual(str(operation.account.operation_cost_position), "15.00")

        operation1 = ExperienceData.objects.get(pk=1)

        self.assertEqual(str(operation1.account.operation_cost_position), "10.00")


    def test_update_equity_on_buy(self):
        create_stocks(self)
        create_buys(self, self.stock)

        self.assertEqual("{0:.2f}".format(self.buy1.account.equity), "7992.35")

    def test_update_equity_on_sell(self):
        create_stocks(self)
        create_buys(self, self.stock)
        create_sells(self, self.stock)

        self.assertEqual("{0:.2f}".format(self.sell1.account.equity), "7992.35")
