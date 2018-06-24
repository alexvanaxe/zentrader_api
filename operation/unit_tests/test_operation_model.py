from datetime import datetime

from django.test.testcases import TestCase

from operation.models import ExperienceData
from account.models import Account
from stock.unit_tests.stock_mocks import create_stocks
from account.unit_tests.account_mocks import create_account

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
