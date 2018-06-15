from datetime import datetime

from django.test.testcases import TestCase

from operation.models import ExperienceData
from stock.unit_tests.stock_mocks import create_stocks


class OperationModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_stocks(cls)


class OperationModelTest(OperationModelTestCase):
    def test_create(self):
        operation = ExperienceData.objects.create(stock=self.stock,
                                             date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                             amount=1000, price=30)

        self.assertIsNotNone(operation.creation_date)
