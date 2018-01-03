from datetime import datetime

from django.test.testcases import TestCase

from operation.models import Operation, OperationType
from stock.unit_tests.stock_mocks import create_stocks
from operation.unit_tests.operation_type_mocks import create_operation_types


class OperationModelTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_stocks(cls)
        create_operation_types(cls)


class OperationModelTest(OperationModelTestCase):
    def test_create(self):
        operation = Operation.objects.create(stock=self.stock, operation_type=self.operationType,
                                             date=datetime.strptime('2017-06-30T15:52:30', '%Y-%m-%dT%H:%M:%S'),
                                             amount=1000, price=30)

        self.assertIsNotNone(operation.creation_date)