from datetime import datetime
from django.test.testcases import TestCase

from ir_br.models import calculate_ir_base_value, calculate_results
from operation.unit_tests.operation_mocks import create_day_trades, create_ir_operations, create_operations
from stock.unit_tests.stock_mocks import create_stocks
from account.unit_tests.account_mocks import create_account
from operation.models import SellData


class IRTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        create_account(cls)
        create_stocks(cls)
        create_operations(cls, cls.stock)


class IRTest(IRTestCase):

    def test_ir_valued(self):
        create_ir_operations(self, self.stock2)
        create_day_trades(self, self.stock2)
        self.assertEqual(str(calculate_ir_base_value(reference_date=datetime.strptime('2017-06-30T15:52:30',
                                                                                      '%Y-%m-%dT%H:%M:%S'))), "17273.84")

    def test_is_day_trade(self):
        create_ir_operations(self, self.stock2)
        create_day_trades(self, self.stock2)

        self.assertEqual(str(calculate_ir_base_value(reference_date=datetime.strptime('2017-06-30T15:52:30',
                                                                                      '%Y-%m-%dT%H:%M:%S'))), "17273.84")


    def test_calculate_results(self):
        create_ir_operations(self, self.stock2)
        reference_date = datetime.strptime('2017-06-25T15:52:30',
                                           '%Y-%m-%dT%H:%M:%S')
        sell_operation_query = SellData.objects.filter(date__lte=reference_date).exclude(date__lte=datetime.strptime('%d-%d-01' % (reference_date.year, reference_date.month), '%Y-%m-%d'))
        results = calculate_results(sell_operation_query)

        try:
            result = next(results)
        except StopIteration:
            self.assertTrue(False)

        self.assertEqual(str(result[1]), "46100.00")
